# Image Handling

Reference for processing extracted images from PDFs.

## Identify Content vs Branding

### Branding/Icon Images (Exclude)

- Very small: 32x32, 48x48, 64x64 pixels
- Repeated on every page (watermarks, headers)
- Company logos, social media icons
- Navigation arrows, bullet graphics

### Content Images (Include)

- Larger dimensions: 200+ pixels in either dimension
- Diagrams, charts, graphs
- Screenshots, photos
- Tables rendered as images
- Mathematical figures, circuit diagrams

### Quick Size Check

```bash
cat /home/claude/extracted/metadata.json | grep -A5 '"images"'
```

Look for patterns:
- Multiple 32x32 images = branding icons (exclude)
- Images 400x300, 500x400 = content (include)

## View and Describe Images

```bash
# List extracted images
ls /home/claude/extracted/images/

# View an image
view /home/claude/extracted/images/page001_img001.png
```

## Convert Markers to Markdown

```markdown
<!-- Raw extraction marker -->
<!-- IMAGE: images/page001_img001.png (400x300px) -->

<!-- Convert to proper markdown -->
![Figure 1: Diagram showing voltage-current relationship](./images/page001_img001.png)
```

## Write Descriptive Alt Text

After viewing each image, write alt text that:
- Describes what the image shows
- Captures key visible information
- Helps readers who cannot see the image

**Examples:**
```markdown
![Figure 1: Graph showing exponential decay of radioactive isotope over time](./images/page001_img001.png)
![Figure 2: Circuit diagram with resistor R1 in series with capacitor C1](./images/page002_img001.png)
![Table 1: Comparison of properties for different materials](./images/page003_img001.png)
```

## Reposition Based on Context

The script estimates positions, but look for contextual clues:

**Image follows (place after this text):**
- "as shown below"
- "see the diagram below"
- "the following figure"
- "illustrated here"

**Image precedes (place before this text):**
- "as shown above"
- "the diagram above shows"
- "in the figure above"

**Example repositioning:**
```markdown
<!-- Before: marker placed by estimation -->
<!-- IMAGE: images/page003_img001.png -->

The ER diagram below shows the relationships between tables.

<!-- After: moved to match "below" reference -->
The ER diagram below shows the relationships between tables.

![Figure 1: ER diagram showing Customer, Order, Product relationships](./images/page003_img001.png)
```

**When no textual clues exist:**
- Place diagrams after the paragraph introducing the concept
- Place tables near data discussions
- Place screenshots near UI descriptions

## Copy Images to Output

```bash
mkdir -p /mnt/user-data/outputs/images/
cp /home/claude/cleaned_document.md /mnt/user-data/outputs/
cp -r /home/claude/extracted/images/* /mnt/user-data/outputs/images/
```

## Handle Missing or Corrupt Images

If an image fails to extract:
- Note in output: `[Image could not be extracted]`
- Check `metadata.json` for extraction errors
- Inform user which images were problematic

## Base64 Embedding (Optional)

For single self-contained file (increases file size significantly):

```markdown
![Figure 1: Description](data:image/png;base64,iVBORw0KGgo...)
```

Only use if specifically requested.
