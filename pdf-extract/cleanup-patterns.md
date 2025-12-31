# Cleanup Patterns Reference

Patterns for identifying noise in extracted PDF content.

> **Usage:** These patterns help Claude recognise what to skip when manually rewriting clean content. Do not use these as regex patterns or script inputs.

## Contents

- [Repeated Element Detection](#repeated-element-detection)
- [Non-Content Elements](#non-content-elements)
- [Source-Specific Patterns](#source-specific-patterns)
- [Text Artifact Fixes](#text-artifact-fixes)

---

## Repeated Element Detection

Identify text appearing on multiple pages (footers, headers, watermarks):

**Detection rules:**
1. Identical or near-identical text appearing 3+ times
2. Text at consistent positions (start/end of page markers)
3. Patterns with incrementing numbers (page counters)

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
{Document Title} — repeated at top
{Chapter/Section Name} — repeated
{Company Logo Text}
```

---

## Non-Content Elements

**Always remove:**
- Standalone page numbers (`5`, `Page 5`, `**5**`)
- TOC page references (`Chapter 1 .................. 5`)
- "Your notes" placeholder sections
- Navigation instructions ("Click here", "See page X")
- Print/download prompts
- Social media links
- QR code references
- Subscription/signup prompts

**Remove if not relevant:**
- Copyright notices
- License statements (CC BY, etc.)
- Disclaimer boilerplate
- Terms and conditions references

---

## Source-Specific Patterns

### Save My Exams (SME)

```
© Save My Exams – AI Powered Revision Notes...
Get more and ace your exams at savemyexams.com
Your notes
[savemyexams.com](https://www.savemyexams.com)
**{page_number}**
```

### Physics & Maths Tutor (PMT)

```
https://bit.ly/pmt-cc
https://bit.ly/pmt-edu
www.pmt.education
This work by PMT Education is licensed under CC BY-NC-ND 4.0
________________________________________ (decorative lines)
```

### Generic Educational Material

```
DRAFT — DO NOT DISTRIBUTE
SAMPLE CHAPTER
PREVIEW ONLY
Answer key on page {N}
```

---

## Text Artifact Fixes

### Hyphenation

| Before | After |
|--------|-------|
| `~~-~~` | `-` |
| `~~−~~` | `−` |
| `con-\ntinue` | `continue` |

### Special Characters

Remove zero-width spaces: `\u200b`, `\u200c`, `\u200d`, `\ufeff`

### Whitespace

| Issue | Fix |
|-------|-----|
| 4+ consecutive blank lines | Max 2 blank lines |
| Trailing whitespace | Remove |
| Multiple spaces | Single space |
