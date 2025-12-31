---
name: pdf-extract
description: Extract and clean PDF content to markdown format. Use when the user uploads a PDF file and wants to convert it to clean, readable markdown. Handles text extraction, image extraction, metadata capture, and intelligent content cleanup. Removes repeated footers, watermarks, page numbers, branding, and reorganizes fragmented content into coherent structure.
---

# PDF Content Extraction Skill

Extract PDF content to clean, organized markdown with maximum fidelity.

## Workflow Overview

1. **Extract**: Run `extract_pdf.py` to get raw content + metadata
2. **Analyse**: Review extracted content for patterns and issues
3. **Clean**: Remove noise (footers, watermarks, branding)
4. **Organise**: Restructure fragmented content into logical flow
5. **Output**: Deliver clean markdown to user

## Step 1: Extract Raw Content

```bash
python /mnt/skills/user/pdf-extract/scripts/extract_pdf.py /mnt/user-data/uploads/{filename}.pdf /home/claude/extracted/
```

**Output structure:**
```
/home/claude/extracted/
├── {filename}.md      # Raw markdown with YAML frontmatter
├── metadata.json      # Structured metadata
└── images/            # Extracted images (if any)
```

**Script options:**
- `--pages 1-10` — Extract specific page range
- `--method pymupdf4llm` — Force primary extractor (better formatting)
- `--method pymupdf` — Force fallback extractor (more reliable for scanned PDFs)
- `--min-image-size 100` — Skip images smaller than 100px

## Step 2: Analyse Extracted Content

```bash
cat /home/claude/extracted/{filename}.md
```

**Check YAML frontmatter for:**
- `extraction_method` — Which extractor was used
- `total_pages` — Document length
- `has_outline` — Whether bookmarks exist
- `total_images` — Number of images to reference

**Identify patterns requiring cleanup:**

| Pattern | Examples | Action |
|---------|----------|--------|
| Repeated footers | "© Company", "Page X of Y" | Remove all |
| Watermarks | "DRAFT", bit.ly links | Remove |
| Page artifacts | Standalone numbers | Remove |
| Fragmented text | Split sentences | Rejoin |

## Step 3: Content Cleanup

Apply cleanup rules based on detected patterns.

**Reference:** See [cleanup-patterns.md](references/cleanup-patterns.md) for:
- Repeated element detection and removal
- Source-specific patterns (Save My Exams, PMT, etc.)
- Text artifact fixes (hyphenation, whitespace, characters)

## Step 4: Content Organisation

### Rejoin Fragmented Content

**Sentences split at line breaks:**
```markdown
<!-- Before -->
A database management system (DBMS) is software that
manages databases and provides users with an interface.

<!-- After -->
A database management system (DBMS) is software that manages databases and provides users with an interface.
```

**Detection rules:**
- Line ends without sentence-ending punctuation (`. ! ? :`)
- Next line starts with lowercase
- Next line continues the same thought

**Do NOT rejoin:**
- Code blocks
- List items
- Table cells
- Headings followed by body text

### Fix Malformed Tables

**Reference:** See [table-formatting.md](references/table-formatting.md) for:
- Misaligned columns
- Missing delimiters
- Duplicate headers from page breaks
- Tables split across pages

### Handle Images

If images were extracted (check `total_images` in YAML header):

**Reference:** See [image-handling.md](references/image-handling.md) for:
- Distinguishing content from branding images
- Writing descriptive alt text
- Repositioning based on context clues
- Copying images to output

**Quick workflow:**
```bash
# View extracted images
ls /home/claude/extracted/images/
view /home/claude/extracted/images/page001_img001.png

# Convert markers to proper markdown
![Figure 1: Description based on image content](./images/page001_img001.png)
```

### Apply Consistent Formatting

**Headings:**
- Use hierarchy consistently (# → ## → ###)
- Don't skip levels

**Lists:**
- Use consistent markers
- Maintain proper nesting

**Paragraphs:**
- Single blank line between paragraphs
- Remove orphan lines

## Step 5: Output Clean Markdown

### Structure

```markdown
# {Document Title}

{Brief description if helpful}

## {First Major Section}

{Clean content...}

---

*Source: {original filename} | Extracted: {date}*
```

### Quality Checklist

- [ ] No repeated footers/headers
- [ ] No standalone page numbers
- [ ] No broken sentences
- [ ] Headings follow logical hierarchy
- [ ] Tables intact and readable
- [ ] Images have descriptive alt text
- [ ] Image paths are correct (`./images/filename.png`)

### Save and Present

**With images:**
```bash
mkdir -p /mnt/user-data/outputs/images/
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/{filename}_clean.md
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

**Without images:**
```bash
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/{filename}_clean.md
```

Present with summary of:
- Pages and images extracted
- Types of noise removed
- Any issues noted

## Special Cases

### Scanned/Image-based PDFs

If extraction produces minimal text:
- Check `extraction_method` in metadata
- Inform user the PDF appears scanned
- Suggest OCR tools if needed

### Multi-column Layouts

pymupdf4llm handles columns reasonably well. Verify:
- Text isn't interleaved incorrectly
- Reading order is logical

### Very Large Documents (50+ pages)

1. Extract in ranges: `--pages 1-25`, then `--pages 26-50`
2. Process sections separately
3. Combine cleaned sections at end

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "File not found" | Wrong path | Check `/mnt/user-data/uploads/` |
| "Invalid PDF header" | Not a PDF | Inform user |
| "Extraction failed" | Protection/corruption | Try `--method pymupdf` |
| Empty output | Scanned PDF | Inform user, suggest OCR |

## Example Session

**User uploads:** `Physics_Chapter_5.pdf`

```bash
# 1. Extract
python /mnt/skills/user/pdf-extract/scripts/extract_pdf.py \
    /mnt/user-data/uploads/Physics_Chapter_5.pdf \
    /home/claude/extracted/

# 2. Read and identify patterns
cat /home/claude/extracted/Physics_Chapter_5.md
# Found: SME branding (12x), "Your notes" (12x), 3 images

# 3. View images for alt text
view /home/claude/extracted/images/page002_img001.png

# 4. Clean: remove branding, rejoin paragraphs, add alt text

# 5. Output
mkdir -p /mnt/user-data/outputs/images/
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

**Summary to user:**
> Extracted 12 pages. Removed Save My Exams branding and page numbers. Included 3 figures with captions.
> 
> **Note:** Keep the `images/` folder alongside the markdown for images to display.
