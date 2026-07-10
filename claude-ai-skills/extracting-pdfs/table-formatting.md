# Table Formatting Reference

Fixes for common table extraction issues.

## Contents

- [Misaligned Columns](#misaligned-columns)
- [Missing Delimiters](#missing-delimiters)
- [Tables as Plain Text](#tables-as-plain-text)
- [Merged Cell Issues](#merged-cell-issues)
- [Repeated Headers](#repeated-headers)

---

## Misaligned Columns

```markdown
<!-- Before -->
| Field | Type | Description |
|---|---|---|
| id | INT | Primary key |
| name | VARCHAR(50) | User's full name which may be quite long |

<!-- After (optional cleanup for readability) -->
| Field | Type        | Description                              |
|-------|-------------|------------------------------------------|
| id    | INT         | Primary key                              |
| name  | VARCHAR(50) | User's full name which may be quite long |
```

---

## Missing Delimiters

```markdown
<!-- Before: broken structure -->
| Method | Description
|--------|------------
| GET | Retrieve data
| POST Submit data

<!-- After: fixed -->
| Method | Description   |
|--------|---------------|
| GET    | Retrieve data |
| POST   | Submit data   |
```

---

## Tables as Plain Text

When complex tables extract as jumbled text, reconstruct or convert:

**Option 1: Rebuild as table**
```markdown
| Name  | Type        | Description      |
|-------|-------------|------------------|
| id    | INT         | Primary key      |
| name  | VARCHAR(50) | User's full name |
| email | VARCHAR(100)| Contact email    |
```

**Option 2: Convert to definition list**
```markdown
**Field definitions:**
- **id**: INT - Primary key
- **name**: VARCHAR(50) - User's full name
- **email**: VARCHAR(100) - Contact email
```

Use definition lists when table format doesn't fit well.

---

## Merged Cell Issues

Tables with spanning cells often extract poorly.

**Options:**
1. Split into separate simple tables
2. Add notes explaining relationships
3. Convert to nested lists

```markdown
<!-- Complex table with spans → simplified -->

**Input Devices:**
- Keyboard, Mouse, Scanner

**Output Devices:**
- Monitor, Printer, Speakers

**Storage Devices:**
- HDD, SSD, USB Drive
```

---

## Repeated Headers

Tables split across pages may have duplicate headers:

```markdown
<!-- Before: header appears twice -->
| Name  | Type |
|-------|------|
| id    | INT  |
| Name  | Type |
| email | VARCHAR |

<!-- After: remove duplicate -->
| Name  | Type    |
|-------|---------|
| id    | INT     |
| email | VARCHAR |
```
