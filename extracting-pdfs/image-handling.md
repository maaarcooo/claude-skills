# Image Handling Reference

Guide for processing extracted images.

## Contents

- [Content vs Branding Images](#content-vs-branding-images)
- [Viewing and Describing Images](#viewing-and-describing-images)
- [Converting Markers to Markdown](#converting-markers-to-markdown)
- [Repositioning Images](#repositioning-images)
- [Output Structure](#output-structure)

---

## Content vs Branding Images

Check image dimensions in `metadata.json` to distinguish:

### Branding/Icons (exclude)

- Very small: 32x32, 48x48, 64x64 pixels
- Repeated on every page
- Company logos, social media icons
- Navigation arrows, bullet graphics

### Content Images (include)

- Larger: 200+ pixels in either dimension
- Diagrams, charts, graphs
- Screenshots, photos
- Tables rendered as images
- Mathematical figures, circuit diagrams

**Quick filter:** Use `--min-image-size 100` to auto-skip small icons:
```bash
python extract_pdf.py document.pdf --min-image-size 100
```

---

## Viewing and Describing Images

Use `view` tool to see each image:

```bash
view /home/claude/extracted/images/page001_img001.png
```

Write descriptive alt text capturing:
- What the image shows (diagram, graph, photo)
- Key information visible
- Context for readers who cannot see it

**Examples:**
```markdown
![Graph showing exponential decay of radioactive isotope over time](./images/page001_img001.png)

![Circuit diagram with resistor R1 in series with capacitor C1](./images/page002_img001.png)

![ER diagram showing Customer, Order, and Product relationships](./images/page003_img001.png)
```

---

## Converting Markers to Markdown

Replace HTML comment markers with proper syntax:

```markdown
<!-- Before (raw extraction) -->
<!-- IMAGE: images/page003_img001.png (450x280px, middle of page) -->

<!-- After (clean markdown) -->
![Figure 1: Description based on viewing the image](./images/page003_img001.png)
```

---

## Repositioning Images

The script estimates positions, but adjust based on context clues:

### Clues indicating image follows

- "as shown below"
- "see the diagram below"
- "the following figure"
- "illustrated here"

### Clues indicating image precedes

- "as shown above"
- "the diagram above"
- "in the figure above"

### Example

```markdown
<!-- Before: marker from estimation -->
<!-- IMAGE: images/page003_img001.png (middle of page) -->

The ER diagram below shows the table relationships.

<!-- After: moved to match "below" -->
The ER diagram below shows the table relationships.

![Figure 1: ER diagram showing table relationships](./images/page003_img001.png)
```

### Fallback rules (no textual clues)

- Place diagrams after paragraph introducing the concept
- Place tables near data discussions
- Place screenshots near UI descriptions

---

## Output Structure

**With images:**
```bash
mkdir -p /mnt/user-data/outputs/images/
cp /home/claude/cleaned.md /mnt/user-data/outputs/
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

**Result:**
```
/mnt/user-data/outputs/
├── document_clean.md
└── images/
    ├── page001_img001.png
    └── page002_img001.png
```

**Note to user:** The `images/` folder must stay alongside the markdown file for images to display.

---

## Handling Issues

| Issue | Solution |
|-------|----------|
| Image fails to extract | Note `[Image could not be extracted]` |
| Corrupt image file | Check `metadata.json` for errors |
| Wrong position | Use textual clues to reposition |
| Missing alt text | View image and describe content |
