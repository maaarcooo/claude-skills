---
name: pdf-to-markdown-converter
description: Convert PDF files to markdown format using visual PDF understanding or image OCR. Use when asked to convert a PDF to markdown, extract PDF content to markdown, transcribe a PDF, or prepare PDF content for further processing. Preserves all text, structure, tables, and equations. Outputs as a markdown file.
---

# PDF to Markdown Converter

Faithfully convert PDF content to markdown format using visual PDF capability or image OCR.

## Process

1. Read every page of the PDF using visual PDF understanding or image OCR
2. Transcribe all content faithfully — this is conversion, not summarisation
3. Preserve document structure: headings, lists, tables, formatting
4. Output as markdown file matching the PDF filename

## Conversion Rules

**Complete transcription**: Include ALL text content. Do not summarise or omit.

**Preserve structure**:
- Headings → `#`, `##`, `###` (match hierarchy from source)
- Bold text → `**bold**`
- Italic text → `*italic*`
- Bullet lists → `-` or `*`
- Numbered lists → `1.`, `2.`, etc.

**Tables**: Convert to markdown table format:
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

**Equations/formulas**: Use LaTeX notation:
- Inline: `$E = mc^2$`
- Block: `$$F = ma$$`

**Diagrams/images**: Describe in a blockquote with [DIAGRAM] prefix:
```markdown
> [DIAGRAM]: Description of what the diagram shows, including labels and key information.
```

**Remove repeated footers**: Omit recurring footer content such as brand names, website links, copyright notices, page numbers, and other boilerplate that appears on multiple pages.

**Page breaks**: Optionally insert `---` between major sections if helpful for navigation.

## Output

Markdown file named to match the source PDF (e.g., `Topic Name.md`).

## Quality Checklist

- [ ] Every page processed
- [ ] All text content included (no omissions)
- [ ] Headings hierarchy preserved
- [ ] Tables correctly formatted
- [ ] Equations in LaTeX notation
- [ ] Diagrams described with key details
- [ ] Document structure matches original