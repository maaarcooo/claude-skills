# Content Cleanup Patterns

Reference for identifying and removing noise from extracted PDF content.

## Repeated Elements

Identify text appearing 3+ times or at consistent positions (page start/end).

### Common Footer Patterns

```
© {Year} {Company Name}
www.{domain}.com
Page {N} of {M}
All rights reserved
{Company} - {Product Line}
```

### Common Header Patterns

```
{Document Title} — repeated at top of each page
{Chapter/Section Name} — repeated headers
{Company Logo Text}
```

## Non-Content Elements

**Always remove:**
- Standalone page numbers (lines containing only "5" or "Page 5")
- Table of contents page references ("Chapter 1 .................. 5")
- "Your notes" or blank placeholder sections
- Navigation instructions ("Click here", "See page X")
- Print/download prompts
- Social media links and handles
- QR code references
- Subscription/signup prompts

**Remove if not relevant:**
- Copyright notices
- License statements (CC BY, etc.)
- Disclaimer boilerplate
- Terms and conditions references

## Source-Specific Patterns

### Save My Exams (SME)

```
© Save My Exams – [content continues]
Get more and ace your exams at savemyexams.com
Your notes
[savemyexams.com](...)
**{page_number}**
```

### Physics & Maths Tutor (PMT)

```
https://bit.ly/pmt-cc
https://bit.ly/pmt-edu
www.pmt.education
This work by PMT Education is licensed under CC BY-NC-ND 4.0
________________________________________  (decorative lines)
```

### Generic Educational Material

```
DRAFT — DO NOT DISTRIBUTE
SAMPLE CHAPTER
PREVIEW ONLY
Answer key on page {N}
```

## Text Artifacts

### Hyphenation Issues

| Pattern | Fix |
|---------|-----|
| `~~-~~` | `-` |
| `~~−~~` | `−` |
| `con-\ntinue` | `continue` |

### Character Issues

| Pattern | Action |
|---------|--------|
| Zero-width spaces (`\u200b`, `\u200c`, `\u200d`, `\ufeff`) | Remove |
| Multiple spaces | Single space |
| Tab characters in running text | Single space |

### Whitespace Issues

| Pattern | Fix |
|---------|-----|
| 4+ consecutive blank lines | 2 blank lines max |
| Trailing whitespace | Remove |
| Leading whitespace (non-intentional) | Remove |
