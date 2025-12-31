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

Run the extraction script on the uploaded PDF:

```bash
python /mnt/skills/user/pdf-extract/scripts/extract_pdf.py /mnt/user-data/uploads/{filename}.pdf /home/claude/extracted/
```

**Output structure:**
```
/home/claude/extracted/
├── {filename}.md      # Raw markdown with YAML frontmatter
├── metadata.json      # Structured metadata (JSON)
└── images/            # Extracted images (if any)
```

**Script options:**
- `--pages 1-10` — Extract specific page range
- `--method pymupdf4llm` — Force primary extractor (better formatting)
- `--method pymupdf` — Force fallback extractor (more reliable for scanned PDFs)

## Step 2: Read and Analyse Extracted Content

Read the extracted markdown file:

```bash
cat /home/claude/extracted/{filename}.md
```

**Check the YAML frontmatter for:**
- `extraction_method` — Which extractor was used
- `total_pages` — Document length
- `has_outline` — Whether bookmarks exist (helps with structure)
- `total_images` — Number of images to reference

**Identify content patterns requiring cleanup:**

| Pattern Type | Examples | Action |
|--------------|----------|--------|
| Repeated footers | "© Company Name", "Page X of Y" | Remove all instances |
| Watermarks | "DRAFT", "CONFIDENTIAL", bit.ly links | Remove |
| Branding | Website URLs, social media handles | Remove unless relevant |
| Page artifacts | Standalone page numbers, headers | Remove |
| Navigation text | "Contents", "Back to top" | Remove |
| Fragmented text | Split sentences, orphaned words | Rejoin and reflow |

## Step 3: Content Cleanup Rules

Apply these cleanup operations to the extracted content:

### 3.1 Remove Repeated Elements

Identify and remove text that appears on every page or most pages:

**Common footer patterns:**
```
© {Year} {Company Name}
www.{domain}.com
Page {N} of {M}
All rights reserved
{Company} - {Product Line}
```

**Common header patterns:**
```
{Document Title} — repeated at top of each page
{Chapter/Section Name} — repeated headers
{Company Logo Text}
```

**Detection method:**
1. Look for identical or near-identical text blocks appearing 3+ times
2. Check text appearing at consistent positions (start/end of page markers)
3. Look for patterns with incrementing numbers (page counters)

### 3.2 Remove Non-Content Elements

**Always remove:**
- Standalone page numbers (e.g., lines containing only "5" or "Page 5")
- Table of contents page references (e.g., "Chapter 1 .................. 5")
- "Your notes" or blank placeholder sections
- Navigation instructions ("Click here", "See page X")
- Print/download prompts
- Social media links and handles
- QR codes references
- Subscription/signup prompts

**Remove if not relevant to content:**
- Copyright notices
- License statements (CC BY, etc.)
- Disclaimer boilerplate
- Terms and conditions references

### 3.3 Clean Source-Specific Patterns

**Save My Exams (SME) patterns:**
```
© Save My Exams – [content continues]
Get more and ace your exams at savemyexams.com
Your notes
[savemyexams.com](...)
**{page_number}**
```

**Physics & Maths Tutor (PMT) patterns:**
```
https://bit.ly/pmt-cc
https://bit.ly/pmt-edu
www.pmt.education
This work by PMT Education is licensed under CC BY-NC-ND 4.0
________________________________________  (decorative lines)
```

**Generic educational material:**
```
DRAFT — DO NOT DISTRIBUTE
SAMPLE CHAPTER
PREVIEW ONLY
Answer key on page {N}
```

### 3.4 Fix Text Artifacts

**Hyphenation issues:**
- `~~-~~` → `-` (strikethrough hyphens)
- `~~−~~` → `−` (strikethrough minus signs)
- Words split across lines: `con-\ntinue` → `continue`

**Character issues:**
- Zero-width spaces: `\u200b`, `\u200c`, `\u200d`, `\ufeff` → remove
- Multiple spaces → single space
- Tab characters in running text → single space

**Whitespace issues:**
- 4+ consecutive blank lines → 2 blank lines maximum
- Trailing whitespace on lines → remove
- Leading whitespace (except intentional indentation) → remove

## Step 4: Content Organisation

### 4.1 Assess Document Structure

**Check if content needs reorganisation:**
- Are paragraphs split mid-sentence across page breaks?
- Are list items separated by page artifacts?
- Are tables broken across pages?
- Is the logical flow disrupted by extracted noise?

### 4.2 Reconstruct Logical Flow

**Rejoin split paragraphs:**
```markdown
<!-- Before -->
This is the beginning of a paragraph that was
<!-- PAGE 2 END -->
<!-- PAGE 3 START -->
split across two pages in the PDF.

<!-- After -->
This is the beginning of a paragraph that was split across two pages in the PDF.
```

**Rejoin split lists:**
```markdown
<!-- Before -->
1. First item
2. Second item
<!-- PAGE BREAK -->
3. Third item

<!-- After -->
1. First item
2. Second item
3. Third item
```

**Reconstruct tables:**
If a table is split across pages, merge the rows into a single table.

### 4.3 Apply Consistent Formatting

**Headings:**
- Use heading hierarchy consistently (# → ## → ###)
- Don't skip levels (no # followed directly by ###)
- Remove redundant heading numbering if using markdown headers

**Lists:**
- Use consistent markers (all `-` or all `*` for unordered)
- Maintain proper nesting with indentation
- Ensure numbered lists use sequential numbers

**Paragraphs:**
- Ensure single blank line between paragraphs
- Remove orphan lines (single words on their own line)
- Merge related short paragraphs if appropriate

### 4.4 Handle Images

If images were extracted (check `total_images` in YAML header), handle them properly:

#### 4.4.1 View Extracted Images

Use the `view` tool to see each image and understand its content:

```bash
# List extracted images
ls /home/claude/extracted/images/

# View an image (Claude can see it visually)
view /home/claude/extracted/images/page001_img001.png
```

#### 4.4.2 Convert Markers to Proper Markdown

Replace HTML comment markers with proper markdown image syntax:

```markdown
<!-- Raw extraction marker -->
<!-- IMAGE: images/page001_img001.png (400x300px) -->

<!-- Clean version - convert to proper markdown image -->
![Figure 1: Diagram showing the relationship between voltage and current](./images/page001_img001.png)
```

#### 4.4.3 Write Descriptive Alt Text

After viewing each image, write meaningful alt text that:
- Describes what the image shows (diagrams, graphs, photos, equations)
- Captures key information visible in the image
- Helps readers who cannot see the image understand its content

**Examples:**
```markdown
![Figure 1: Graph showing exponential decay of radioactive isotope over time](./images/page001_img001.png)

![Figure 2: Circuit diagram with resistor R1 in series with capacitor C1](./images/page002_img001.png)

![Table 1: Comparison of properties for different materials](./images/page003_img001.png)
```

#### 4.4.4 Position Images Correctly

- Place images near the text that references them
- If the original position is unclear, place after the paragraph that introduces the concept
- For figures referenced by number ("see Figure 3"), ensure numbering matches

#### 4.4.5 Copy Images to Output

**Important:** When saving the final markdown, also copy the images folder:

```bash
# Create output structure
mkdir -p /mnt/user-data/outputs/images/

# Copy cleaned markdown
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/

# Copy all images
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

The final output structure should be:
```
/mnt/user-data/outputs/
├── document.md           # Clean markdown with image references
└── images/               # All extracted images
    ├── page001_img001.png
    ├── page002_img001.png
    └── ...
```

#### 4.4.6 Alternative: Embed Images as Base64 (Single File)

If user prefers a single self-contained file, images can be embedded as base64:

```markdown
![Figure 1: Description](data:image/png;base64,iVBORw0KGgo...)
```

However, this significantly increases file size. Only use if specifically requested.

#### 4.4.7 Handle Missing or Corrupt Images

If an image fails to extract or appears corrupt:
- Note it in the output: `[Image could not be extracted]`
- Check `metadata.json` for image extraction errors
- Inform user which images were problematic

## Step 5: Output Clean Markdown

### 5.1 Structure the Final Document

```markdown
# {Document Title}

{Brief description or context if helpful}

## {First Major Section}

{Clean content...}

## {Second Major Section}

{Clean content...}

---

*Source: {original filename} | Extracted: {date}*
```

### 5.2 Quality Checklist

Before delivering to user, verify:

- [ ] No repeated footers/headers remain
- [ ] No standalone page numbers
- [ ] No watermarks or branding (unless relevant)
- [ ] No broken sentences or orphaned words
- [ ] Headings follow logical hierarchy
- [ ] Lists are properly formatted
- [ ] Tables are intact and readable
- [ ] **Images: All markers converted to proper markdown syntax**
- [ ] **Images: Alt text is descriptive and accurate**
- [ ] **Images: Images folder copied to outputs (if applicable)**
- [ ] **Images: Relative paths are correct (`./images/filename.png`)**
- [ ] Overall flow is coherent and readable

### 5.3 Save and Present

**If document has images:**
```bash
# Create output directory with images
mkdir -p /mnt/user-data/outputs/images/

# Copy cleaned markdown
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/{filename}_clean.md

# Copy images folder
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

**If document has no images:**
```bash
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/{filename}_clean.md
```

Present to user with brief summary of:
- What was extracted (pages, images)
- What was cleaned (types of noise removed)
- Any issues or limitations noted
- If images included, remind user the `images/` folder is required for images to display

## Special Cases

### Scanned/Image-based PDFs

If extraction produces minimal text:
1. Check `extraction_method` in metadata — if `pymupdf (fallback)` was used, content may be limited
2. Inform user the PDF appears to be scanned/image-based
3. Suggest OCR tools if higher quality extraction is needed

### Multi-column Layouts

pymupdf4llm handles multi-column layouts reasonably well, but verify:
- Text from columns isn't interleaved incorrectly
- Reading order makes logical sense
- Manually reorder if columns were merged incorrectly

### Forms and Fillable PDFs

Check `metadata.json` for `has_forms`. If true:
- Form field content may need special handling
- Labels and values might be separated
- Consider presenting as key-value pairs

### Very Large Documents (50+ pages)

For large documents:
1. Consider extracting in page ranges: `--pages 1-25`, then `--pages 26-50`
2. Process sections separately to manage context
3. Combine cleaned sections at the end

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "File not found" | Wrong path | Check `/mnt/user-data/uploads/` for actual filename |
| "Invalid PDF header" | Corrupted or not a PDF | Inform user file is invalid |
| "Extraction failed" | PDF protection or corruption | Try `--method pymupdf` fallback |
| Empty/minimal output | Scanned PDF without OCR | Inform user, suggest OCR |

## Example Cleanup Session

**User uploads:** `Physics_Chapter_5.pdf`

```bash
# 1. Extract
python /mnt/skills/user/pdf-extract/scripts/extract_pdf.py \
    /mnt/user-data/uploads/Physics_Chapter_5.pdf \
    /home/claude/extracted/

# 2. Read raw output
cat /home/claude/extracted/Physics_Chapter_5.md

# 3. Identify patterns (example findings):
#    - "© Save My Exams" appears 12 times
#    - "Your notes" appears 12 times  
#    - Page numbers 1-12 appear standalone
#    - www.savemyexams.com appears in footer
#    - 3 images extracted

# 4. If images exist, view them to write alt text
view /home/claude/extracted/images/page002_img001.png
# (Claude sees: diagram of electric circuit with battery and resistors)

view /home/claude/extracted/images/page005_img001.png
# (Claude sees: graph of voltage vs current)

# 5. Clean content:
#    - Remove all SME branding
#    - Remove "Your notes" sections
#    - Remove standalone page numbers
#    - Rejoin split paragraphs
#    - Convert image markers to proper markdown with alt text:
#      ![Figure 1: Electric circuit with battery and two resistors in series](./images/page002_img001.png)
#      ![Figure 2: Linear graph showing voltage vs current relationship (Ohm's Law)](./images/page005_img001.png)

# 6. Output clean version with images
mkdir -p /mnt/user-data/outputs/images/
# Save cleaned markdown to /mnt/user-data/outputs/Physics_Chapter_5_clean.md
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

**Summary to user:**
> Extracted and cleaned 12 pages from Physics_Chapter_5.pdf. Removed Save My Exams branding, page numbers, and "Your notes" placeholders. Included 3 figures with descriptive captions. The content is now clean markdown with proper heading structure.
> 
> **Note:** The `images/` folder contains the extracted figures — keep it alongside the markdown file for images to display correctly.
