---
name: pdf-extract
description: Extract and clean PDF content to markdown format. Use when the user uploads a PDF file and wants to convert it to clean, readable markdown. Handles text extraction, image extraction, metadata capture, and intelligent content cleanup. Removes repeated footers, watermarks, page numbers, branding, and reorganizes fragmented content into coherent structure.
---

# PDF Content Extraction Skill

Extract PDF content to clean, organized markdown.

## Workflow

1. **Extract** — Run script to get raw content + metadata
2. **Analyse** — Review for patterns and issues
3. **Clean** — **Manually** remove noise (footers, watermarks, branding)
4. **Organise** — Restructure fragmented content
5. **Output** — Deliver clean markdown

> **Note:** Only Step 1 uses a script. Steps 2–5 are performed manually by Claude reading and rewriting content. Do not write cleanup scripts.

## Step 1: Extract

```bash
python /mnt/skills/user/pdf-extract/scripts/extract_pdf.py \
    /mnt/user-data/uploads/{filename}.pdf \
    /home/claude/extracted/
```

**Options:**
| Option | Description |
|--------|-------------|
| `--pages 1-10` | Extract specific page range |
| `--method pymupdf4llm` | Force primary extractor (better formatting) |
| `--method pymupdf` | Force fallback (more reliable for scanned PDFs) |
| `--min-image-size 100` | Skip images smaller than 100px (filters icons) |

**Output:**
```
/home/claude/extracted/
├── {filename}.md      # Raw markdown with YAML frontmatter
├── metadata.json      # Structured metadata
└── images/            # Extracted images (if any)
```

## Step 2: Analyse

Read the extracted markdown:
```bash
cat /home/claude/extracted/{filename}.md
```

**Check YAML frontmatter for:**
- `extraction_method` — Which extractor was used
- `total_pages` — Document length
- `has_outline` — Bookmarks exist (helps with structure)
- `total_images` — Number of images

**Identify issues requiring cleanup:**
- Repeated footers/headers on every page
- Watermarks, branding, page numbers
- Fragmented sentences across line breaks
- Malformed tables
- Image markers needing repositioning

## Step 3: Clean

> **IMPORTANT: Manual cleanup only.**
> - Do NOT write Python scripts to clean the content
> - Do NOT use sed, awk, or regex replacement commands
> - Do NOT copy-paste the raw content and run substitutions
> 
> Instead: Read the extracted content, understand it, then write a clean version from scratch, omitting the noise as you write.

**Why manual?** Each PDF has unique patterns. Claude makes better contextual decisions than automated rules — knowing what's noise vs. legitimate content, handling edge cases, and preserving meaning.

**Process:**
1. Read through the extracted markdown completely
2. Identify repeated noise (footers, headers, branding, page numbers)
3. Note the actual content structure (sections, flow, key information)
4. Write the clean output directly, skipping noise as you go

Load references as needed for pattern recognition:

**Repeated elements & source-specific patterns:**
See [cleanup-patterns.md](references/cleanup-patterns.md)
- Use when: footers, headers, SME/PMT branding detected

**Text fragmentation:**
See [sentence-reflow.md](references/sentence-reflow.md)
- Use when: sentences split across lines or pages

**Table issues:**
See [table-formatting.md](references/table-formatting.md)
- Use when: tables have missing delimiters, broken structure

**Image handling:**
See [image-handling.md](references/image-handling.md)
- Use when: document contains images to process

## Step 4: Organise

While writing the clean output, apply these formatting principles:

### Heading Hierarchy

- Use `#` → `##` → `###` consistently
- Don't skip levels
- Remove redundant numbering if using markdown headers

### Paragraph Flow

- Single blank line between paragraphs
- Remove orphan lines (single words alone)
- Merge related short paragraphs

### Image Placement

Convert markers to proper markdown:
```markdown
<!-- Before -->
<!-- IMAGE: images/page003_img001.png (450x280px) -->

<!-- After -->
![Figure 1: Description](./images/page003_img001.png)
```

View each image with `view` tool to write accurate alt text.

## Step 5: Output

### Write Clean File

After reading and mentally processing the extracted content, write the clean markdown directly to a file:

```bash
# Write clean content to file (Claude creates this content)
cat > /mnt/user-data/outputs/{filename}_clean.md << 'EOF'
# Document Title

[Clean content goes here - written by Claude, not copied]

EOF
```

Or use the `create_file` tool to write the clean content directly.

### Copy Images (if applicable)

```bash
mkdir -p /mnt/user-data/outputs/images/
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

### Quality Check

- [ ] No repeated footers/headers
- [ ] No standalone page numbers
- [ ] No watermarks or branding
- [ ] Sentences properly rejoined
- [ ] Tables intact and readable
- [ ] Images converted to markdown syntax
- [ ] Heading hierarchy logical

### Summary to User

Include:
- Pages extracted
- What was cleaned (types of noise removed)
- Images included (remind about `images/` folder requirement)
- Any limitations noted

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "File not found" | Wrong path | Check `/mnt/user-data/uploads/` |
| "Invalid PDF header" | Not a PDF | Inform user file is invalid |
| "Extraction failed" | Protected/corrupted | Try `--method pymupdf` |
| Empty output | Scanned PDF | Inform user, suggest OCR |

## Special Cases

### Scanned/Image PDFs

If `extraction_method` shows `pymupdf (fallback)` with minimal text:
- PDF is likely scanned/image-based
- Inform user OCR tools may be needed

### Large Documents (50+ pages)

Consider extracting in ranges:
```bash
python extract_pdf.py doc.pdf ./out1/ --pages 1-25
python extract_pdf.py doc.pdf ./out2/ --pages 26-50
```

### Multi-Column Layouts

Verify reading order makes sense. pymupdf4llm handles columns reasonably but may interleave incorrectly.

## Output Format

Final markdown structure:
```markdown
# {Document Title}

## {First Section}

{Clean content...}

## {Second Section}

{Clean content...}

---

*Source: {filename}.pdf | Extracted: {date}*
```
