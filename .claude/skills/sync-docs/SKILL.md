---
name: sync-docs
description: Sync documentation and screenshots to Pylon knowledge base. Handles two modes: (1) Upload screenshots to Pylon CDN and return CloudFront URLs, (2) Sync markdown documentation to Pylon KB with proper collection assignment. Uses Python scripts for Pylon API integration.
---

# Sync Documentation to Pylon

Sync screenshots and documentation to Pylon knowledge base.

## Purpose

This skill handles Pylon integration in two modes:

1. **Upload Mode**: Upload screenshots to Pylon CDN, get CloudFront URLs
2. **Sync Mode**: Convert markdown to HTML, sync to Pylon KB with correct collection

## Prerequisites

1. **Pylon Configuration**: API key, KB ID, collection IDs in config.yaml
2. **Python Environment**: Pylon integration scripts installed
3. **Screenshots Captured**: For upload mode
4. **Documentation Written**: For sync mode

## Mode 1: Upload Screenshots

### When to Use

After screenshots are captured, before creating documentation. You need CloudFront URLs to embed in documentation.

### Input

- Feature name
- Screenshots directory (from config.yaml)
- Screenshot filenames

### Process

#### Step 1: Locate Screenshots

Find the captured screenshots:

```bash
ls -lh output/screenshots/[feature]-*.png
```

**Verify:**
- Screenshots exist
- Filenames are correct
- File sizes are reasonable (not 0 bytes)

#### Step 2: Upload to Pylon

Use the Pylon upload script for each screenshot:

```bash
cd /path/to/max-doc-ai

python3 scripts/pylon/upload.py \
  --image output/screenshots/[feature]-overview.png \
  --alt "[Feature Name] overview"
```

**For multiple screenshots**, upload each one:

```bash
# Screenshot 1
python3 scripts/pylon/upload.py \
  --image output/screenshots/[feature]-overview.png \
  --alt "[Feature Name] overview"

# Screenshot 2
python3 scripts/pylon/upload.py \
  --image output/screenshots/[feature]-detail.png \
  --alt "[Feature Name] detailed view"

# ... continue for all screenshots
```

#### Step 3: Collect CloudFront URLs

The upload script will output CloudFront URLs like:

```
📤 Uploading: feature-overview.png
   ✅ Uploaded: https://d1234abcd.cloudfront.net/attachments/abc123/feature-overview.png
```

**Save all URLs** - you'll need them for the documentation.

#### Step 4: Create URL Mapping

Document the mapping:

```markdown
## CloudFront URLs for [Feature Name]

1. **[feature]-overview.png**
   - CloudFront URL: https://d1234abcd.cloudfront.net/attachments/abc123/feature-overview.png
   - Alt text: [Feature Name] overview

2. **[feature]-detail.png**
   - CloudFront URL: https://d1234abcd.cloudfront.net/attachments/abc123/feature-detail.png
   - Alt text: [Feature Name] detailed view

[... continue for all screenshots ...]
```

#### Step 5: Provide URLs to Next Step

Return the CloudFront URLs so they can be used in documentation:

```
✅ Screenshot Upload Complete

Uploaded [X] screenshots to Pylon CDN.

CloudFront URLs:
- feature-overview: https://cloudfront.url/1.png
- feature-detail: https://cloudfront.url/2.png
[... list all ...]

These URLs should be used in the documentation markdown.
```

---

## Mode 2: Sync Documentation

### When to Use

After documentation is written with embedded CloudFront URLs. This publishes the documentation to Pylon knowledge base.

### Input

- Feature name
- Category (must match config.yaml collections)
- Documentation file path
- Title and slug for the article

### Process

#### Step 1: Verify Documentation File

Check that documentation file exists and is valid:

```bash
cat output/features/YYYY-MM-DD_[feature-slug]/[feature-slug].md
```

**Verify:**
- File exists
- Valid markdown
- No H1 heading (starts with H2)
- Screenshots use CloudFront URLs
- Content is complete

#### Step 2: Determine Article Key

Create a unique key for state tracking:

**Pattern:** `[category]-[feature-slug]`

**Examples:**
- `features-dashboards`
- `integrations-slack`
- `getting-started-quickstart`

This key is used to track whether the article already exists in Pylon.

#### Step 3: Sync to Pylon

Use the Pylon sync script:

```bash
cd /path/to/max-doc-ai

python3 scripts/pylon/sync.py \
  --file output/features/YYYY-MM-DD_[feature-slug]/[feature-slug].md \
  --key [category]-[feature-slug] \
  --title "[Feature Name]" \
  --slug "[feature-slug]" \
  --collection [category]
```

**Example:**
```bash
python3 scripts/pylon/sync.py \
  --file output/features/2025-12-22_dashboards/dashboards.md \
  --key features-dashboards \
  --title "Dashboards" \
  --slug "dashboards" \
  --collection features
```

#### Step 4: Monitor Sync Process

The script will:

1. Read markdown file
2. Convert to HTML
3. Wrap images in React components (required by Pylon)
4. Check if article exists (via state file)
5. Create new or update existing article
6. Set collection_id (CRITICAL: must be set during creation)
7. Return article URLs

**Watch for:**
```
📄 Syncing: dashboards.md
🔄 Converting markdown to HTML...
   ✅ 3 images with React wrappers
✨ Creating new article...
   Collection: features (abc-123-collection-id)
   ✅ Created article ID: xyz-789-article-id
💾 State updated: features-dashboards
```

#### Step 5: Extract Article URLs

The sync will output:

```
✅ Article synced successfully!
   Public URL: https://yourproduct-kb.help.usepylon.com/articles/dashboards
   Internal URL: https://app.usepylon.com/docs/[kb-id]/articles/[article-id]
```

**Save both URLs:**
- **Public URL**: For customer-facing announcements
- **Internal URL**: For editing and management

#### Step 6: Verify in Pylon

Optional but recommended - verify the article in Pylon:

1. Open the public URL in browser
2. Check that:
   - Article title is correct
   - Content is properly formatted
   - Screenshots are visible and sized correctly
   - Images have React wrappers (inspect HTML if needed)
   - Article is in the correct collection

#### Step 7: Document Results

Provide a summary:

```markdown
## Documentation Synced: [Feature Name]

**Article Title:** [Feature Name]
**Slug:** [feature-slug]
**Category/Collection:** [category]
**State Key:** [category]-[feature-slug]

### URLs:

**Public (for announcements):**
https://yourproduct-kb.help.usepylon.com/articles/[slug]

**Internal (for editing):**
https://app.usepylon.com/docs/[kb-id]/articles/[article-id]

### Technical Details:

- Markdown file: output/features/YYYY-MM-DD_[feature-slug]/[feature-slug].md
- Images: [X] screenshots with React wrappers
- Collection ID: [collection-id]
- Article ID: [article-id]
- Created/Updated: [timestamp]

### Next Steps:

Use the public URL in customer announcements.
```

---

## Pylon Integration Details

### React Image Wrappers

**CRITICAL**: Pylon requires images to be wrapped in a specific React component structure. The converter script handles this automatically.

**Structure:**
```html
<div class="react-renderer node-imageBlock" contenteditable="false" draggable="true">
  <div data-node-view-wrapper="" style="white-space: normal;">
    <button aria-label="Preview image: Preview" class="inline-block w-full cursor-zoom-in">
      <div class="ml-auto mr-auto mx-auto" style="width: 100%;">
        <div contenteditable="false">
          <img class="block" alt="..." src="https://cloudfront.url/image.png">
        </div>
      </div>
    </button>
  </div>
</div>
```

**Why this matters:**
- Without this structure, images won't render in Pylon
- The structure is NOT optional
- Must be exact format

### Collection ID Requirement

**CRITICAL**: The `collection_id` MUST be set when creating an article. It cannot be reliably added later via PATCH requests.

This is why the sync script:
1. Checks state to see if article exists
2. If new, creates with `collection_id` set
3. If existing, updates via PATCH (collection already set)

### State Tracking

Pylon's API doesn't provide a "list all articles" endpoint, so we maintain our own state file:

**Location:** `demo/docs/sync-state.json`

**Structure:**
```json
{
  "knowledge_base_id": "...",
  "articles": {
    "features-dashboards": {
      "article_id": "...",
      "collection_id": "...",
      "public_url": "...",
      "internal_url": "...",
      "synced_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

### URL Encoding

CloudFront URLs often contain `&` characters in query parameters. Pylon requires **unencoded** ampersands (`&` not `&amp;`). The converter handles this automatically.

## Configuration

Pylon settings in `config.yaml`:

```yaml
pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  author_user_id: "${PYLON_AUTHOR_ID}"
  api_base: "https://api.usepylon.com"
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
    integrations: "${COLLECTION_INTEGRATIONS_ID}"
```

**Collection IDs:**
- Create collections in Pylon web UI first
- Copy the collection ID from the URL
- Add to config.yaml
- Collection names must match exactly

## Troubleshooting

### Upload Failures

**Issue:** Screenshot upload fails with 401 Unauthorized

**Solution:**
- Check PYLON_API_KEY is set correctly in .env
- Verify API key has necessary permissions
- Try regenerating API key in Pylon settings

**Issue:** Upload succeeds but no URL returned

**Solution:**
- Check Pylon API response format hasn't changed
- Verify network connectivity
- Check image file is valid PNG/JPG

### Sync Failures

**Issue:** Article creation fails with "Collection not found"

**Solution:**
- Verify collection ID in config.yaml is correct
- Check collection exists in Pylon
- Ensure collection ID matches the category name

**Issue:** Images don't appear in Pylon article

**Solution:**
- Verify CloudFront URLs are accessible
- Check React wrappers are applied (run with --validate flag)
- Ensure URLs use unencoded & characters
- Inspect HTML in Pylon to see actual structure

**Issue:** Article created but in wrong collection

**Solution:**
- Delete article from Pylon UI
- Remove from state file: `python3 scripts/utils/state.py --delete [key]`
- Fix collection ID in config.yaml
- Sync again

### State Issues

**Issue:** Sync thinks article exists but it doesn't

**Solution:**
```bash
# Check state
python3 scripts/utils/state.py --summary

# Remove incorrect entry
python3 scripts/utils/state.py --delete [article-key]

# Sync again
```

**Issue:** State file corrupted

**Solution:**
- Backup existing: `cp demo/docs/sync-state.json demo/docs/sync-state.json.backup`
- Delete state file
- Re-sync all articles (they'll be created fresh)

## Integration with Release Workflow

This skill is used twice in the release workflow:

1. Capture screenshots (capture-screenshots skill)
2. ✅ **Upload screenshots to CDN** ← Mode 1: You are here first
3. Create documentation (update-product-doc skill) ← Uses CloudFront URLs
4. ✅ **Sync documentation to Pylon** ← Mode 2: You are here second
5. Create announcements (create-changelog skill) ← Uses public article URL

The public article URL from Mode 2 should be provided to the create-changelog skill.
