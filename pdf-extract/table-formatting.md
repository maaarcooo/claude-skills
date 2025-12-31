# Table Formatting Fixes

Reference for fixing malformed tables from PDF extraction.

## Misaligned Columns

```markdown
<!-- Before -->
| Field | Type | Description |
|---|---|---|
| id | INT | Primary key |
| name | VARCHAR(50) | User's full name which may be quite long |

<!-- After -->
| Field | Type        | Description                              |
|-------|-------------|------------------------------------------|
| id    | INT         | Primary key                              |
| name  | VARCHAR(50) | User's full name which may be quite long |
```

## Missing Cell Delimiters

```markdown
<!-- Before -->
| Method | Description
|--------|------------
| GET | Retrieve data
| POST Submit data

<!-- After -->
| Method | Description   |
|--------|---------------|
| GET    | Retrieve data |
| POST   | Submit data   |
```

## Table Converted to Plain Text

If a complex table was extracted as jumbled text:
1. Identify the data structure from context
2. Reconstruct as a proper markdown table
3. Or use definition list for simple key-value data:

```markdown
**Field definitions:**
- **id**: INT - Primary key
- **name**: VARCHAR(50) - User's full name
- **email**: VARCHAR(100) - Contact email
```

## Merged Cells Extracted Incorrectly

Options for tables with spanning cells:
1. Split into separate simple tables
2. Add notes explaining the relationship
3. Convert to nested lists if clearer

## Duplicate Headers (Page Break)

```markdown
<!-- Before -->
| Name | Type |
|------|------|
| id | INT |
| Name | Type |
| email | VARCHAR |

<!-- After -->
| Name  | Type    |
|-------|---------|
| id    | INT     |
| email | VARCHAR |
```

## Split Tables Across Pages

```markdown
<!-- Before: table split with header repeated -->
| Name | Type |
|------|------|
| id | INT |
| name | VARCHAR |

| Name | Type |
|------|------|
| email | VARCHAR |
| created | DATE |

<!-- After: merged into single table -->
| Name    | Type    |
|---------|---------|
| id      | INT     |
| name    | VARCHAR |
| email   | VARCHAR |
| created | DATE    |
```
