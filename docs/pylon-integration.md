# Pylon Integration Guide

Complete technical reference for the Pylon Knowledge Base integration in max-doc-AI.

## Overview

[Pylon](https://usepylon.com) is a customer knowledge base platform that provides:
- **Knowledge Base Articles** - Searchable, organized documentation
- **Collections** - Categorical organization of articles
- **Attachments API** - CDN-hosted images via CloudFront
- **Public URLs** - Shareable article links for customers

max-doc-AI uses Pylon's REST API to:
1. Upload screenshots to Pylon's CDN
2. Create/update documentation articles
3. Organize content by collections
4. Track sync state to prevent duplicates

## Architecture

### Components

```
┌─────────────────┐
│  Claude Skills  │
│  (orchestrate)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Python Scripts              │
│  ┌──────────────────────────────┐  │
│  │  pylon/upload.py             │  │ → Upload screenshots
│  │  - PylonUploader             │  │
│  ├──────────────────────────────┤  │
│  │  pylon/sync.py               │  │ → Sync documentation
│  │  - PylonSync                 │  │
│  ├──────────────────────────────┤  │
│  │  pylon/converter.py          │  │ → Markdown → HTML
│  │  - MarkdownConverter         │  │
│  ├──────────────────────────────┤  │
│  │  utils/state.py              │  │ → Track synced articles
│  │  - StateManager              │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Pylon API     │
│  ─────────────  │
│  /attachments   │ ← Screenshot upload (multipart/form-data)
│  /articles      │ ← Article CRUD (JSON)
└─────────────────┘
```

## Authentication

### API Key Setup

1. **Generate API Key:**
   - Go to https://app.usepylon.com/settings/api-keys
   - Click "Create API Key"
   - Name it (e.g., "max-doc-AI")
   - Copy the key (starts with `pylon_api_`)

2. **Store Securely:**
   ```bash
   # In .env file
   PYLON_API_KEY=pylon_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Reference in Config:**
   ```yaml
   # In config.yaml
   pylon:
     api_key: "${PYLON_API_KEY}"
   ```

### Authentication Method

All API requests use Bearer token authentication:

```python
headers = {
    'Authorization': f'Bearer {api_key}'
}
```

**Security Notes:**
- Never commit API keys to version control
- API keys have full access to your Knowledge Base
- Rotate keys periodically
- Use environment variables for sensitive data

## Knowledge Base Structure

### Collections

Collections organize articles by category:

```
Knowledge Base (kb_id)
├── Collection: getting-started
│   ├── Article: Quickstart Guide
│   └── Article: Installation
├── Collection: features
│   ├── Article: Dashboards
│   ├── Article: Automation
│   └── Article: Integrations
└── Collection: integrations
    ├── Article: Slack Integration
    └── Article: API Webhooks
```

**Configuration:**
```yaml
# config.yaml
pylon:
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
    integrations: "${COLLECTION_INTEGRATIONS_ID}"

documentation:
  categories:
    - getting-started
    - features
    - integrations
```

**Important:**
- Collection names in `documentation.categories` must match keys in `pylon.collections`
- Collection IDs are UUIDs (e.g., `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
- Collections must be created in Pylon UI before use
- Get collection IDs from the URL when viewing a collection in Pylon

### Creating Collections

1. Log into Pylon web interface
2. Navigate to your Knowledge Base
3. Click "Collections" → "New Collection"
4. Enter collection name (e.g., "Features")
5. Copy the collection ID from the URL
6. Add to `.env`:
   ```bash
   COLLECTION_FEATURES_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

## Attachments API (Screenshots)

### Upload Process

Screenshots are uploaded to Pylon's Attachments API which stores them on CloudFront CDN.

**API Endpoint:**
```
POST https://api.usepylon.com/attachments
```

**Request Format:**
```python
# Multipart form data
files = {
    'file': (filename, file_handle, 'image/png')
}
data = {
    'alt_text': 'Dashboard overview',
    'caption': 'Main dashboard view'
}
```

**Response:**
```json
{
  "data": {
    "id": "attachment-id",
    "url": "https://d1234567.cloudfront.net/path/to/image.png",
    "filename": "dashboard-overview.png",
    "content_type": "image/png",
    "size": 125678
  }
}
```

**Usage in Code:**

```python
from pylon.upload import PylonUploader

uploader = PylonUploader()
result = uploader.upload_image(
    image_path='screenshots/dashboard.png',
    alt_text='Dashboard overview',
    caption='Main dashboard with metrics'
)

if result:
    cloudfront_url = result['url']
    print(f"Image uploaded: {cloudfront_url}")
```

**Key Points:**
- Returns permanent CloudFront URLs
- Images are publicly accessible via URL
- Supports PNG and JPEG formats
- No size limit documented (tested up to 5MB)
- Alt text improves accessibility
- Captions appear in Pylon UI

## Articles API (Documentation)

### Article Lifecycle

```
1. Create → 2. Update → 3. Publish → 4. Track
```

### Creating Articles

**API Endpoint:**
```
POST https://api.usepylon.com/knowledge-bases/{kb_id}/articles
```

**Request Payload:**
```json
{
  "title": "Dashboard Feature",
  "slug": "dashboards",
  "body_html": "<h1>Dashboards</h1><p>Feature overview...</p>",
  "author_user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "collection_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "is_published": true,
  "publish_updated_body_html": true
}
```

**Response:**
```json
{
  "data": {
    "id": "article-id",
    "title": "Dashboard Feature",
    "slug": "dashboards",
    "url": "https://kb.usepylon.com/docs/{kb_id}/dashboards",
    "public_url": "https://docs.yourproduct.com/dashboards",
    "collection_id": "collection-id",
    "is_published": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Critical Requirements:**
- `collection_id` **MUST** be set during creation
- Cannot reliably add collection after creation
- `slug` must be unique within the Knowledge Base
- `author_user_id` required for attribution

### Updating Articles

**API Endpoint:**
```
PATCH https://api.usepylon.com/knowledge-bases/{kb_id}/articles/{article_id}
```

**Request Payload:**
```json
{
  "title": "Updated Dashboard Feature",
  "body_html": "<h1>Updated content...</h1>",
  "publish_updated_body_html": true
}
```

**When to Update vs Create:**
- **Update** if article exists (check state file)
- **Create** for new articles
- State tracking prevents duplicates

### Article HTML Format

Pylon accepts HTML content with React component wrappers for images:

**Standard Markdown Image:**
```markdown
![Dashboard overview](https://d123.cloudfront.net/dashboard.png)
```

**Converted to Pylon Format:**
```html
<ReactImage
  src="https://d123.cloudfront.net/dashboard.png"
  alt="Dashboard overview"
/>
```

**Conversion Process:**

```python
from pylon.converter import MarkdownConverter

converter = MarkdownConverter()
html = converter.convert_to_pylon_html(markdown_content)
```

**Supported HTML Tags:**
- Headers: `<h1>` to `<h6>`
- Paragraphs: `<p>`
- Lists: `<ul>`, `<ol>`, `<li>`
- Links: `<a>`
- Images: `<ReactImage>` component
- Code: `<code>`, `<pre>`
- Emphasis: `<strong>`, `<em>`

## State Tracking

### Purpose

The state file (`sync-state.json`) tracks which articles have been synced to Pylon to:
- Prevent duplicate article creation
- Enable updates to existing articles
- Track CloudFront URLs
- Record sync history

### State File Format

```json
{
  "last_updated": "2024-01-15T10:30:00Z",
  "articles": {
    "features/dashboards": {
      "pylon_article_id": "article-id-uuid",
      "title": "Dashboard Feature",
      "slug": "dashboards",
      "collection": "features",
      "url": "https://kb.usepylon.com/docs/kb-id/dashboards",
      "public_url": "https://docs.yourproduct.com/dashboards",
      "synced_at": "2024-01-15T10:30:00Z",
      "file_path": "demo/docs/product_documentation/features/dashboards.md",
      "images": [
        {
          "filename": "dashboard-overview.png",
          "cloudfront_url": "https://d123.cloudfront.net/dashboard-overview.png",
          "pylon_id": "attachment-id"
        }
      ]
    }
  }
}
```

### State Operations

**Check if Article Exists:**
```python
from utils.state import StateManager

state = StateManager()
article_key = 'features/dashboards'

if state.article_exists(article_key):
    article_data = state.get_article(article_key)
    article_id = article_data['pylon_article_id']
    print(f"Article exists with ID: {article_id}")
```

**Record New Article:**
```python
state.record_article(
    key='features/dashboards',
    pylon_article_id='article-id',
    title='Dashboard Feature',
    slug='dashboards',
    collection='features',
    url='https://kb.usepylon.com/...',
    public_url='https://docs.yourproduct.com/...',
    file_path='demo/docs/product_documentation/features/dashboards.md',
    images=[...]
)
```

**View State Summary:**
```bash
python3 scripts/utils/state.py --summary
```

**Clear State (for testing):**
```bash
python3 scripts/utils/state.py --clear
```

## Workflow Examples

### Complete Feature Release

```python
# 1. Capture screenshots
from screenshot.capture import ScreenshotCapturer

with ScreenshotCapturer() as capturer:
    capturer.navigate('https://app.product.com/dashboards')
    capturer.capture('dashboard-overview')

# 2. Upload to Pylon CDN
from pylon.upload import PylonUploader

uploader = PylonUploader()
result = uploader.upload_image(
    'screenshots/dashboard-overview.png',
    alt_text='Dashboard overview'
)
cloudfront_url = result['url']

# 3. Create documentation
markdown_content = f"""
# Dashboards

Visualize your metrics with customizable dashboards.

![Dashboard overview]({cloudfront_url})

## Features
- Real-time data
- Custom widgets
- Export capabilities
"""

# 4. Convert and sync to Pylon
from pylon.converter import MarkdownConverter
from pylon.sync import PylonSync

converter = MarkdownConverter()
html = converter.convert_to_pylon_html(markdown_content)

sync = PylonSync()
article = sync.create_article(
    title='Dashboards',
    slug='dashboards',
    body_html=html,
    collection_name='features'
)

print(f"Article published: {article['public_url']}")

# 5. Record in state
from utils.state import StateManager

state = StateManager()
state.record_article(
    key='features/dashboards',
    pylon_article_id=article['id'],
    title='Dashboards',
    slug='dashboards',
    collection='features',
    url=article['url'],
    public_url=article['public_url'],
    file_path='demo/docs/product_documentation/features/dashboards.md',
    images=[{'filename': 'dashboard-overview.png', 'cloudfront_url': cloudfront_url}]
)
```

### Update Existing Article

```python
from utils.state import StateManager
from pylon.sync import PylonSync

# Check if article exists
state = StateManager()
article_key = 'features/dashboards'

if state.article_exists(article_key):
    article_data = state.get_article(article_key)

    # Update the article
    sync = PylonSync()
    updated = sync.update_article(
        article_id=article_data['pylon_article_id'],
        title='Dashboards (Updated)',
        body_html='<h1>New content</h1>'
    )

    print(f"Article updated: {updated['url']}")
else:
    print("Article doesn't exist, create it first")
```

## Error Handling

### Common Errors

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key"
}
```
**Solution:**
- Check `PYLON_API_KEY` in `.env`
- Verify key is active in Pylon settings
- Generate new key if needed

**404 Not Found (Collection):**
```json
{
  "error": "Not found",
  "message": "Collection not found"
}
```
**Solution:**
- Verify collection ID in `.env`
- Check collection exists in Pylon UI
- Copy ID from Pylon URL

**409 Conflict (Duplicate Slug):**
```json
{
  "error": "Conflict",
  "message": "Slug already exists"
}
```
**Solution:**
- Use unique slugs per article
- Check state file for existing slugs
- Update existing article instead of creating new

**422 Unprocessable Entity:**
```json
{
  "error": "Validation failed",
  "message": "collection_id is required"
}
```
**Solution:**
- Always include `collection_id` during creation
- Cannot add collection reliably after creation

### Retry Logic

Built-in retry for transient failures:

```python
import time
import requests

def upload_with_retry(uploader, image_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            return uploader.upload_image(image_path)
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Retry in {wait_time}s...")
            time.sleep(wait_time)
```

## Testing & Validation

### Test Configuration

```bash
# Validate config loads
python3 scripts/config.py

# Test Pylon connection
python3 scripts/pylon/upload.py

# Check state
python3 scripts/utils/state.py --summary
```

### Manual API Testing

```bash
# Test authentication
curl -H "Authorization: Bearer $PYLON_API_KEY" \
  https://api.usepylon.com/knowledge-bases/$PYLON_KB_ID/articles

# Upload test image
curl -X POST https://api.usepylon.com/attachments \
  -H "Authorization: Bearer $PYLON_API_KEY" \
  -F "file=@test-image.png"
```

### Verify Articles in Pylon

1. Log into Pylon web interface
2. Go to Knowledge Base
3. Check articles appear in correct collections
4. Verify images load from CloudFront
5. Test public URLs are accessible

## Best Practices

1. **Always Set Collection During Creation**
   - Include `collection_id` in initial POST request
   - Cannot reliably add later

2. **Use State Tracking**
   - Check state before creating articles
   - Update existing articles instead of duplicating
   - Record all CloudFront URLs

3. **Validate Before Sync**
   - Test markdown locally first
   - Verify CloudFront URLs are accessible
   - Check HTML conversion output

4. **Handle Rate Limits**
   - Implement retry logic with backoff
   - Batch operations when possible
   - Monitor API response times

5. **Keep State Backed Up**
   - Commit `sync-state.json` carefully (contains IDs)
   - Or add to `.gitignore` and back up separately
   - Recreate from Pylon API if lost

6. **Use Consistent Naming**
   - Slugs: lowercase, hyphen-separated
   - File paths: match article keys
   - Collections: match category names

## Troubleshooting

**Problem:** Articles created but not in collections

**Solution:**
- Always set `collection_id` during article creation
- Recreate articles if collection missing
- Cannot reliably patch collection after creation

---

**Problem:** Images don't load in articles

**Solution:**
- Verify CloudFront URLs are public
- Check URL format uses `<ReactImage>` component
- Test URLs directly in browser

---

**Problem:** State file out of sync

**Solution:**
```bash
# Clear state and re-sync
python3 scripts/utils/state.py --clear
# Then re-run sync operations
```

---

**Problem:** Duplicate articles created

**Solution:**
- Check state file before creating
- Use unique slugs
- Query Pylon API to verify article doesn't exist

## API Reference

### Base URL
```
https://api.usepylon.com
```

### Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/attachments` | Upload images to CDN |
| POST | `/knowledge-bases/{kb_id}/articles` | Create article |
| PATCH | `/knowledge-bases/{kb_id}/articles/{article_id}` | Update article |
| GET | `/knowledge-bases/{kb_id}/articles` | List articles |
| GET | `/knowledge-bases/{kb_id}/articles/{article_id}` | Get article |

### Rate Limits

Pylon API rate limits (as of 2024):
- 100 requests per minute per API key
- 1000 requests per hour per API key

*Check Pylon documentation for current limits.*

## Next Steps

- [Setup Guide](setup.md) - Configure Pylon integration
- [Usage Guide](usage.md) - Use the skills
- [Configuration Reference](configuration.md) - All config options

## Resources

- [Pylon Documentation](https://docs.usepylon.com)
- [Pylon API Reference](https://docs.usepylon.com/api)
- [Pylon Dashboard](https://app.usepylon.com)
