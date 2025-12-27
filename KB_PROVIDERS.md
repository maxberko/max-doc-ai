# Knowledge Base Provider System

A generic, extensible architecture for syncing documentation to any knowledge base platform.

## Overview

The KB Provider system provides a unified interface for working with multiple knowledge base platforms (Pylon, Zendesk, Confluence, Notion, etc.) without changing your workflow or scripts.

### Key Benefits

✅ **Provider-Agnostic**: Write once, work with any KB provider
✅ **Easy Switching**: Change providers via config, no code changes
✅ **Extensible**: Add new providers by implementing a simple interface
✅ **Backwards Compatible**: Works with existing Pylon-only configurations
✅ **Type-Safe**: Strong typing with dataclasses and type hints

## Architecture

```
utils/kb_providers/
├── base.py           # Abstract base class (KBProvider)
├── pylon.py          # Pylon implementation
├── zendesk.py        # Zendesk implementation
├── __init__.py       # Provider factory

scripts/kb/
├── sync.py           # Generic sync script
├── upload.py         # Generic upload script
├── __init__.py
```

### Core Components

#### 1. Abstract Base Class (`KBProvider`)

Defines the interface all providers must implement:

```python
class KBProvider(ABC):
    # Article Management
    @abstractmethod
    def create_article(self, article: Article) -> Optional[Article]

    @abstractmethod
    def update_article(self, article_id: str, article: Article) -> bool

    @abstractmethod
    def get_article(self, article_id: str) -> Optional[Article]

    @abstractmethod
    def delete_article(self, article_id: str) -> bool

    @abstractmethod
    def list_articles(self, collection_id: Optional[str] = None) -> List[Article]

    # Image/Attachment Management
    @abstractmethod
    def upload_image(self, image_path: str, alt_text: str = "", caption: str = "") -> Optional[ImageUpload]

    @abstractmethod
    def upload_images_batch(self, images: List[Dict]) -> Dict[str, ImageUpload]

    # Content Conversion (provider-specific)
    @abstractmethod
    def markdown_to_html(self, markdown: str) -> str

    @abstractmethod
    def validate_html(self, html: str) -> tuple[bool, str]

    # Collections/Categories
    @abstractmethod
    def get_collection_id(self, collection_name: str) -> Optional[str]

    @abstractmethod
    def list_collections(self) -> List[Dict]

    # Utility
    @abstractmethod
    def test_connection(self) -> bool
```

#### 2. Data Models

Provider-agnostic data models:

```python
@dataclass
class Article:
    id: Optional[str] = None
    title: str = ""
    slug: str = ""
    body_html: str = ""
    status: ArticleStatus = ArticleStatus.PUBLISHED
    collection_id: Optional[str] = None
    collection_name: Optional[str] = None
    public_url: Optional[str] = None
    internal_url: Optional[str] = None
    author_id: Optional[str] = None
    metadata: Dict = None

@dataclass
class ImageUpload:
    url: str
    filename: str
    alt_text: str = ""
    caption: str = ""
    provider_id: Optional[str] = None
    metadata: Dict = None
```

#### 3. Provider Factory

Instantiates the correct provider:

```python
from utils.kb_providers import get_provider

# Get provider from config
provider = get_provider('pylon', config)

# Use provider
article = Article(title="My Article", body_html="<p>Content</p>")
result = provider.create_article(article)
```

## Configuration

### New Format (Recommended)

```yaml
knowledge_base:
  # Active provider
  provider: "pylon"

  # Provider-specific configurations
  providers:
    pylon:
      api_key: "${PYLON_API_KEY}"
      kb_id: "${PYLON_KB_ID}"
      author_user_id: "${PYLON_AUTHOR_ID}"
      api_base: "https://api.usepylon.com"
      collections:
        getting-started: "col_123"
        features: "col_456"

    zendesk:
      subdomain: "mycompany"
      email: "admin@example.com"
      api_token: "${ZENDESK_API_TOKEN}"
      locale: "en-us"
      categories:
        getting-started: "section_789"
        features: "section_012"
```

### Old Format (Still Supported)

```yaml
pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  # ...
```

The system automatically detects the old format and treats it as `provider: pylon`.

## Usage

### 1. Upload Screenshots

```bash
# Uses provider from config
python3 scripts/kb/upload.py \
  --image output/screenshots/feature-overview.png \
  --alt "Feature overview"

# Override provider
python3 scripts/kb/upload.py \
  --provider zendesk \
  --image output/screenshots/feature-overview.png \
  --alt "Feature overview"
```

### 2. Sync Documentation

```bash
# Uses provider from config
python3 scripts/kb/sync.py \
  --file output/features/2025-12-25_my-feature/my-feature.md \
  --key features-my-feature \
  --title "My Feature" \
  --slug "my-feature" \
  --collection features

# Override provider
python3 scripts/kb/sync.py \
  --provider zendesk \
  --file output/features/2025-12-25_my-feature/my-feature.md \
  --key features-my-feature \
  --title "My Feature" \
  --slug "my-feature" \
  --collection features
```

### 3. Programmatic Usage

```python
from utils.kb_providers import get_provider, Article

# Get provider
provider = get_provider('pylon', {
    'api_key': 'your-key',
    'kb_id': 'your-kb-id',
    # ...
})

# Test connection
if provider.test_connection():
    print("✅ Connected!")

# Upload image
image_result = provider.upload_image(
    'screenshot.png',
    alt_text='Dashboard view'
)
print(f"Uploaded to: {image_result.url}")

# Create article
article = Article(
    title='Getting Started',
    slug='getting-started',
    body_html='<h2>Welcome</h2><p>Content...</p>',
    collection_name='getting-started'
)

result = provider.create_article(article)
print(f"Article created: {result.public_url}")
```

## Supported Providers

### Pylon ✅ Fully Implemented

- Article CRUD operations
- Image upload to CDN (CloudFront URLs)
- React component wrappers for images (required)
- Collection management
- State tracking (Pylon lacks list endpoint)

**Special Features:**
- Automatic React wrapper injection for images
- CloudFront CDN URLs
- Collection ID must be set during creation (not patchable)

### Zendesk ✅ Fully Implemented

- Article CRUD operations
- Image upload to Zendesk CDN
- Section (collection) management
- Multi-locale support
- Brand support

**Special Features:**
- Translation support (multi-locale)
- Brand separation
- Section-based organization

### Coming Soon

- **Confluence** - Atlassian Confluence Cloud
- **Notion** - Notion API v1
- **Intercom** - Intercom Articles
- **GitBook** - GitBook API

## Adding a New Provider

### Step 1: Create Provider Class

Create `utils/kb_providers/yourprovider.py`:

```python
from utils.kb_providers.base import KBProvider, Article, ImageUpload

class YourProvider(KBProvider):
    def __init__(self, config: Dict):
        self.api_key = config['api_key']
        self.base_url = config['base_url']
        # Initialize your provider

    @property
    def provider_name(self) -> str:
        return "yourprovider"

    def create_article(self, article: Article) -> Optional[Article]:
        # Implement article creation
        pass

    def update_article(self, article_id: str, article: Article) -> bool:
        # Implement article update
        pass

    # ... implement all abstract methods
```

### Step 2: Register Provider

In `utils/kb_providers/__init__.py`:

```python
from utils.kb_providers.yourprovider import YourProvider

PROVIDERS = {
    'pylon': PylonProvider,
    'zendesk': ZendeskProvider,
    'yourprovider': YourProvider,  # Add here
}
```

### Step 3: Add Configuration

In `config.example.yaml`:

```yaml
knowledge_base:
  providers:
    yourprovider:
      api_key: "${YOUR_PROVIDER_API_KEY}"
      base_url: "https://api.yourprovider.com"
      # Provider-specific settings
```

### Step 4: Test

```python
from utils.kb_providers import get_provider

provider = get_provider('yourprovider', {
    'api_key': 'test-key',
    'base_url': 'https://api.yourprovider.com'
})

# Test connection
assert provider.test_connection()

# Test article creation
article = Article(title="Test", body_html="<p>Test</p>")
result = provider.create_article(article)
assert result is not None
```

## Provider-Specific Considerations

### HTML Conversion

Different providers have different HTML requirements:

**Pylon:**
```python
def markdown_to_html(self, markdown: str) -> str:
    # Must wrap images in React components
    html = markdown.markdown(markdown)
    html = wrap_images_in_react_components(html)
    return html
```

**Zendesk:**
```python
def markdown_to_html(self, markdown: str) -> str:
    # Standard HTML is fine
    return markdown.markdown(markdown)
```

**Confluence:**
```python
def markdown_to_html(self, markdown: str) -> str:
    # Confluence uses XHTML Storage Format
    html = markdown.markdown(markdown)
    html = convert_to_xhtml(html)
    return html
```

### Image Upload

**Pylon:** Uses `/attachments` endpoint, returns CloudFront URLs
**Zendesk:** Uses `/articles/attachments.json`, returns Zendesk CDN URLs
**Confluence:** Uploads as page attachments, returns Atlassian media URLs

### Collection/Category Handling

**Pylon:** Collections are assigned during article creation only
**Zendesk:** Sections can be changed via API
**Confluence:** Pages exist in spaces with parent-child relationships

## Migration Guide

### From Pylon-Only to Generic

**Before:**
```python
from pylon import sync
syncer = sync.PylonSync()
syncer.sync_article_from_markdown(...)
```

**After:**
```python
from utils.kb_providers import get_provider
from scripts.kb import sync

provider = get_provider('pylon', config)
sync.sync_article_from_markdown('pylon', ...)
```

### Switching Providers

1. Add new provider config to `config.yaml`
2. Update `knowledge_base.provider` setting
3. Re-sync all articles (they'll be created in new provider)
4. Update internal URLs in announcements

**No code changes required!**

## Best Practices

### 1. Use State Tracking

Always use the state file to track article IDs:

```python
from utils import state as state_manager

# Save article
state_manager.save_article('provider:key', article_data)

# Load state
state = state_manager.load_state()
existing = state.get('articles', {}).get('provider:key')
```

### 2. Provider Prefixing

Always prefix state keys with provider name:

```
pylon:features-dashboard
zendesk:features-dashboard
```

This allows syncing the same article to multiple providers.

### 3. Error Handling

```python
provider = get_provider('pylon', config)

if not provider:
    print("❌ Provider initialization failed")
    sys.exit(1)

if not provider.test_connection():
    print("❌ Connection test failed")
    sys.exit(1)

# Continue with operations
```

### 4. Validation

Always validate HTML before syncing:

```python
html = provider.markdown_to_html(markdown)
is_valid, message = provider.validate_html(html)

if not is_valid:
    print(f"❌ Invalid HTML: {message}")
    sys.exit(1)
```

## Troubleshooting

### Provider Not Found

```
❌ Unknown provider: xyz
Available providers: pylon, zendesk
```

**Solution:** Check provider name spelling and ensure it's registered in `PROVIDERS`.

### Configuration Missing

```
❌ Provider 'zendesk' not found in config.yaml
```

**Solution:** Add provider configuration under `knowledge_base.providers.zendesk`.

### Connection Failed

```
❌ Connection test failed
```

**Solution:**
- Verify API credentials
- Check network connectivity
- Ensure API endpoint is correct
- Review provider-specific auth requirements

### HTML Validation Failed

```
❌ Invalid HTML: Found 5 img tags but only 3 React wrappers
```

**Solution:** Check provider's `markdown_to_html` implementation ensures all images are properly converted.

## Performance

### Upload Performance

- **Pylon**: ~500ms per image (includes CloudFront distribution)
- **Zendesk**: ~300ms per image
- **Parallel uploads**: Use `upload_images_batch` for better performance

### Sync Performance

- **Pylon**: ~1-2s per article (includes React conversion)
- **Zendesk**: ~800ms per article
- **Rate limits**: Check provider documentation for API limits

## API Reference

See docstrings in:
- `utils/kb_providers/base.py` - Base interface
- `utils/kb_providers/pylon.py` - Pylon implementation
- `utils/kb_providers/zendesk.py` - Zendesk implementation

## Contributing

To add a new provider:

1. Create provider class in `utils/kb_providers/`
2. Implement all abstract methods from `KBProvider`
3. Add to provider registry
4. Add configuration example
5. Update this documentation
6. Add tests

## License

Part of max-doc-ai project.

---

**Questions?** Open an issue or check the documentation in `.claude/skills/sync-docs/SKILL.md`.
