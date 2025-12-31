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
- `--min-image-size 100` — Skip images smaller than 100px (filters icons/logos)

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

#### 4.2.1 Rejoin Fragmented Sentences

PDF extraction often breaks sentences at visual line endings. Detect and fix these patterns:

**Pattern A: Mid-sentence line breaks (most common)**
```markdown
<!-- Before: sentence split at PDF line wrap -->
A database management system (DBMS) is software that
manages databases and provides users with an interface
to interact with the data stored within them.

<!-- After: rejoined into proper paragraph -->
A database management system (DBMS) is software that manages databases and provides users with an interface to interact with the data stored within them.
```

**Detection rules:**
- Line ends without sentence-ending punctuation (`.` `!` `?` `:`)
- Next line starts with lowercase letter
- Next line continues the same thought

**Pattern B: Hyphenated word splits**
```markdown
<!-- Before -->
The rela-
tional model organises data into tables.

<!-- After -->
The relational model organises data into tables.
```

**Pattern C: Splits across page markers**
```markdown
<!-- Before -->
This concept is fundamental to understanding
<!-- PAGE 5 END -->
<!-- PAGE 6 START -->
how databases maintain referential integrity.

<!-- After -->
This concept is fundamental to understanding how databases maintain referential integrity.
```

**When NOT to rejoin:**
- Intentional line breaks in code blocks
- List items (each item is meant to be separate)
- Table cells
- Headings followed by body text

#### 4.2.2 Rejoin Split Lists

```markdown
<!-- Before -->
1. First item
2. Second item
<!-- PAGE BREAK artifacts -->
3. Third item

<!-- After -->
1. First item
2. Second item
3. Third item
```

#### 4.2.3 Reconstruct Split Tables

If a table is split across pages:

```markdown
<!-- Before: table header repeated on page 2 -->
| Name | Type |
|------|------|
| id | INT |
| name | VARCHAR |

| Name | Type |
|------|------|
| email | VARCHAR |
| created | DATE |

<!-- After: merged into single table -->
| Name | Type |
|------|------|
| id | INT |
| name | VARCHAR |
| email | VARCHAR |
| created | DATE |
```

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

### 4.3.1 Fix Malformed Tables

pymupdf4llm may produce tables with formatting issues. Common problems and fixes:

**Problem A: Misaligned columns**
```markdown
<!-- Before: columns don't align -->
| Field | Type | Description |
|---|---|---|
| id | INT | Primary key |
| name | VARCHAR(50) | User's full name which may be quite long |

<!-- After: proper alignment (optional but cleaner) -->
| Field | Type        | Description                              |
|-------|-------------|------------------------------------------|
| id    | INT         | Primary key                              |
| name  | VARCHAR(50) | User's full name which may be quite long |
```

**Problem B: Missing cell delimiters**
```markdown
<!-- Before: broken table structure -->
| Method | Description
|--------|------------
| GET | Retrieve data
| POST Submit data

<!-- After: fixed delimiters -->
| Method | Description   |
|--------|---------------|
| GET    | Retrieve data |
| POST   | Submit data   |
```

**Problem C: Table converted to plain text**

If a complex table was extracted as jumbled text rather than markdown table:
1. Identify the data structure from context
2. Reconstruct as a proper markdown table
3. Or present as a definition list if table format doesn't fit:

```markdown
<!-- Alternative: definition list for simple key-value data -->
**Field definitions:**
- **id**: INT - Primary key
- **name**: VARCHAR(50) - User's full name
- **email**: VARCHAR(100) - Contact email
```

**Problem D: Merged cells extracted incorrectly**

Tables with merged/spanning cells often extract poorly. Options:
1. Split into separate simple tables
2. Add notes explaining the relationship
3. Convert to nested lists if clearer

**Problem E: Table headers repeated (page break)**
```markdown
<!-- Before: header appears twice -->
| Name | Type |
|------|------|
| id | INT |
| Name | Type |
| email | VARCHAR |

<!-- After: remove duplicate header -->
| Name | Type |
|------|------|
| id | INT |
| email | VARCHAR |
```

### 4.4 Handle Images

If images were extracted (check `total_images` in YAML header), handle them properly:

#### 4.4.1 Identify Content vs Branding Images

Check `metadata.json` or the image dimensions to distinguish content from branding:

**Branding/icon images (typically exclude):**
- Very small: 32x32, 48x48, 64x64 pixels (logos, icons)
- Repeated on every page (watermarks, headers)
- Company logos, social media icons
- Navigation arrows, bullet graphics

**Content images (typically include):**
- Larger dimensions: 200+ pixels in either dimension
- Diagrams, charts, graphs
- Screenshots, photos
- Tables rendered as images
- Mathematical figures, circuit diagrams

**Quick filter by size:**
```bash
# List images with dimensions to identify small icons
cat /home/claude/extracted/metadata.json | grep -A5 '"images"'
```

Look for patterns like:
- Multiple 32x32 images = likely branding icons (exclude)
- Images 400x300, 500x400, etc. = likely content (include)

When copying images to output, only include content images:
```bash
# Example: copy only images larger than 100x100
# (Claude should filter based on metadata.json review)
```

#### 4.4.2 View Extracted Images

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

#### 4.4.4 Reposition Images Based on Context

The script estimates image positions, but they may need adjustment. Look for contextual clues:

**Clue phrases that indicate an image follows:**
- "as shown below"
- "see the diagram below"
- "the following figure"
- "illustrated here"
- "see Figure X"

**Clue phrases that indicate an image precedes:**
- "as shown above"
- "the diagram above shows"
- "in the figure above"
- "as illustrated"

**Repositioning example:**
```markdown
<!-- Before: marker placed by script estimation -->
<!-- IMAGE: images/page003_img001.png (450x280px, middle of page) -->

The Entity-Relationship diagram below shows the relationships
between the Customer, Order, and Product tables.

<!-- After: moved to match "below" reference -->
The Entity-Relationship diagram below shows the relationships
between the Customer, Order, and Product tables.

![Figure 1: ER diagram showing Customer, Order, and Product table relationships](./images/page003_img001.png)
```

**When no textual clues exist:**
- Place diagrams/figures after the paragraph that introduces the concept
- Place tables near data discussions
- Place screenshots near UI/interface descriptions

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
