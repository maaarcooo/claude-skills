# Sentence Reflow Reference

Techniques for rejoining fragmented text when rewriting clean content.

## Contents

- [Mid-Sentence Line Breaks](#mid-sentence-line-breaks)
- [Hyphenated Word Splits](#hyphenated-word-splits)
- [Page Break Splits](#page-break-splits)
- [When NOT to Rejoin](#when-not-to-rejoin)
- [List and Table Reconstruction](#list-and-table-reconstruction)

---

## Mid-Sentence Line Breaks

**Most common issue.** PDF stores text visually, breaking at line endings.

```markdown
<!-- Before -->
A database management system (DBMS) is software that
manages databases and provides users with an interface
to interact with the data stored within them.

<!-- After -->
A database management system (DBMS) is software that manages databases and provides users with an interface to interact with the data stored within them.
```

### Detection Rules

Rejoin when:
- Line ends without sentence punctuation (`. ! ? :`)
- Next line starts with lowercase letter
- Next line continues the same thought

---

## Hyphenated Word Splits

Words split with hyphen at line end:

```markdown
<!-- Before -->
The rela-
tional model organises data into tables.

<!-- After -->
The relational model organises data into tables.
```

Also fix strikethrough artifacts:
- `~~-~~` → `-`
- `~~−~~` → `−`

---

## Page Break Splits

Sentences split across page markers:

```markdown
<!-- Before -->
This concept is fundamental to understanding
<!-- PAGE 5 END -->
<!-- PAGE 6 START -->
how databases maintain referential integrity.

<!-- After -->
This concept is fundamental to understanding how databases maintain referential integrity.
```

---

## When NOT to Rejoin

**Preserve intentional breaks:**

- Code blocks (formatting matters)
- List items (each meant to be separate)
- Table cells
- Headings followed by body text
- Poetry or quoted material with line breaks

---

## List and Table Reconstruction

### Split Lists

```markdown
<!-- Before -->
1. First item
2. Second item
<!-- PAGE artifacts -->
3. Third item

<!-- After -->
1. First item
2. Second item
3. Third item
```

### Split Tables

Merge rows from tables split across pages:

```markdown
<!-- Before: table continues on next page -->
| Name | Type |
|------|------|
| id   | INT  |

| Name  | Type    |
|-------|---------|
| email | VARCHAR |

<!-- After: merged -->
| Name  | Type    |
|-------|---------|
| id    | INT     |
| email | VARCHAR |
```

See [table-formatting.md](table-formatting.md) for more table fixes.
