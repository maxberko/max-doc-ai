# Getting Started with max-doc-ai

Welcome! 👋 Let's get you up and running in **less than 5 minutes**.

## What is max-doc-ai?

max-doc-ai automates your entire product documentation workflow:

- 📸 **Screenshot Capture** - Automatically capture product screenshots using Computer Use
- 📝 **Documentation Generation** - Create comprehensive docs from your codebase
- 🔄 **KB Sync** - Publish to Pylon, Zendesk, or other knowledge bases
- 📣 **Announcements** - Generate customer-facing release notes

**The goal:** Say _"Create a release for [feature]"_ and get back complete, published documentation.

## Quick Start (3 Steps)

### Step 1: Clone & Install

```bash
git clone https://github.com/anthropics/max-doc-ai.git
cd max-doc-ai
```

No dependencies to install! Everything uses Python standard library.

### Step 2: Run Setup Wizard

```bash
python3 scripts/setup.py
```

The setup wizard will:
- ✅ Check your system
- ✅ Help you choose a knowledge base (Pylon, Zendesk, etc.)
- ✅ Collect your API credentials
- ✅ Create configuration files
- ✅ Test the connection
- ✅ Show you what to do next

**It's interactive and friendly** - just answer a few questions!

### Step 3: Verify Everything Works

```bash
python3 scripts/health_check.py
```

This runs a comprehensive health check and tells you if anything needs attention.

## Your First Release

Once setup is complete, you're ready to create your first release:

### Option A: Using Claude

```bash
claude "Create a release for [your feature name]"
```

Claude will:
1. Ask you a few questions about the feature
2. Research your codebase
3. Capture screenshots (if needed)
4. Write comprehensive documentation
5. Sync to your knowledge base
6. Generate announcements

**Everything happens automatically!**

### Option B: Sync Existing Documentation

Already have documentation written? Sync it:

```bash
# Discover what documentation you have
python3 scripts/kb/sync.py discover

# Sync a specific file
python3 scripts/kb/sync.py sync \
  --file path/to/your/doc.md \
  --key category-slug \
  --title "Your Title" \
  --slug "your-slug" \
  --collection features
```

## Understanding the System

### Key Concepts

**1. Knowledge Base Provider**
Where your documentation lives (Pylon, Zendesk, Confluence, etc.). You choose one during setup.

**2. Documentation Inventory**
The system automatically discovers all your documentation files and tracks their sync status.

**3. Skills**
Claude uses "skills" to perform different tasks:
- `create-release` - Complete release workflow
- `capture-screenshots` - Screenshot capture
- `sync-docs` - Upload images and sync documentation
- `update-product-doc` - Create/update documentation
- `create-changelog` - Generate announcements

### File Structure

```
max-doc-ai/
├── output/                           # All generated content goes here
│   ├── features/                     # Feature documentation
│   │   └── YYYY-MM-DD_feature-name/  # Dated folders
│   ├── changelogs/                   # Announcements
│   └── screenshots/                  # Captured screenshots
├── scripts/                          # Tools and scripts
│   ├── setup.py                      # Setup wizard
│   ├── health_check.py               # Health check
│   └── kb/                           # KB sync tools
├── utils/                            # Utility modules
│   ├── kb_providers/                 # Provider implementations
│   ├── doc_inventory.py              # Documentation scanner
│   └── feature_classifier.py         # Feature type detection
├── .claude/                          # Claude configuration
│   └── skills/                       # Skill definitions
├── config.yaml                       # Your configuration
└── .env                              # Your secrets (API keys)
```

## Common Tasks

### Check What Documentation You Have

```bash
python3 scripts/kb/sync.py discover
```

Shows all your documentation files, what's synced, and what needs syncing.

### Check Sync Status

```bash
python3 scripts/kb/sync.py status
```

Detailed status of all documentation, including public URLs.

### Sync a Document

```bash
python3 scripts/kb/sync.py sync \
  --file docs/features/dashboard.md \
  --key features-dashboard \
  --title "Dashboard" \
  --slug "dashboard" \
  --collection features
```

### Validate Skills

```bash
python3 utils/skill_validator.py
```

Ensures all Claude skills are properly registered.

### Run Health Check

```bash
python3 scripts/health_check.py
```

Comprehensive system check with helpful fixes.

## Configuration

Your configuration is split into two files:

### config.yaml - Structure & Settings

```yaml
knowledge_base:
  provider: "pylon"  # Your KB provider
  providers:
    pylon:
      api_key: "${PYLON_API_KEY}"  # References .env
      kb_id: "${PYLON_KB_ID}"
      # ... more settings
```

### .env - Secrets & API Keys

```bash
PYLON_API_KEY=your-actual-api-key
PYLON_KB_ID=your-kb-id
# ... more secrets
```

**Never commit .env to git!** (It's in .gitignore by default)

## Switching Knowledge Base Providers

Want to try a different KB provider?

```bash
# Run setup again
python3 scripts/setup.py

# Choose a different provider
# Your old config is preserved
```

Or edit `config.yaml` manually:

```yaml
knowledge_base:
  provider: "zendesk"  # Changed from "pylon"
  providers:
    pylon:
      # ... keep old config
    zendesk:
      # ... add new config
```

## Troubleshooting

### "Config file not found"

```bash
# Run setup wizard
python3 scripts/setup.py
```

### "Cannot connect to provider"

```bash
# Check your credentials
python3 scripts/health_check.py

# Test connection manually
python3 -c "
import sys; sys.path.insert(0, '.')
from utils.kb_providers import get_provider
import config as cfg

kb = cfg.get_kb_config()
p = get_provider(kb['provider'], kb['config'])
print('Connected!' if p.test_connection() else 'Failed')
"
```

### "Skills not registered"

```bash
# Validate skills
python3 utils/skill_validator.py

# Check settings file
cat .claude/settings.local.json
```

### "Documentation not syncing"

```bash
# Check sync status
python3 scripts/kb/sync.py status

# Try manual sync
python3 scripts/kb/sync.py sync \
  --file path/to/doc.md \
  --key category-slug \
  --title "Title" \
  --slug "slug" \
  --collection category
```

## Advanced Features

### Feature Type Classification

The system automatically detects if screenshots are needed:

- **UI_CHANGE** - New UI → Needs screenshots
- **DATA_ENHANCEMENT** - Backend only → Skip screenshots
- **INFRASTRUCTURE** - Config/tooling → Minimal workflow

This saves time and money!

### Multi-Language Screenshots

Capture the same views in multiple languages:

```python
from utils.multilang_screenshot import MultiLanguageScreenshotCapturer

capturer = MultiLanguageScreenshotCapturer(
    base_url='https://yourapp.com',
    languages=['en', 'fr', 'de'],
    parallel=True  # Faster!
)

capturer.capture_multi_language_views(views)
```

### Progress Tracking

Visual feedback during long operations:

```python
from utils.progress import ProgressTracker

tracker = ProgressTracker(total_steps=5)
tracker.start_step("Research", "Analyzing 247 files")
# ... do work ...
tracker.complete_step("Research", "Found 12 relevant files")
```

### Documentation Discovery

Automatically finds and catalogs all documentation:

```python
from utils.doc_inventory import DocumentInventory

inventory = DocumentInventory()
inventory.scan()
inventory.print_summary()
```

## Getting Help

### Documentation

- **KB Providers**: See [KB_PROVIDERS.md](KB_PROVIDERS.md)
- **Release Workflow**: See [RELEASE_WORKFLOW_INTEGRATION.md](RELEASE_WORKFLOW_INTEGRATION.md)
- **New Features**: See [NEW_FEATURES.md](NEW_FEATURES.md)

### Commands Reference

```bash
# Setup & Health
python3 scripts/setup.py              # Interactive setup
python3 scripts/health_check.py       # System health check

# Documentation Discovery
python3 scripts/kb/sync.py discover   # Find all documentation
python3 scripts/kb/sync.py status     # Check sync status
python3 utils/doc_inventory.py        # Detailed inventory

# Syncing
python3 scripts/kb/sync.py sync       # Sync a document
python3 scripts/kb/upload.py          # Upload images

# Validation
python3 utils/skill_validator.py      # Validate skills
python3 utils/feature_classifier.py   # Test classifier
```

### Support

- **Issues**: https://github.com/anthropics/max-doc-ai/issues
- **Discussions**: https://github.com/anthropics/max-doc-ai/discussions

## What's Next?

Now that you're set up:

1. ✅ Run `python3 scripts/kb/sync.py discover` to see what documentation you have
2. ✅ Try creating a release: `claude "Create a release for [feature]"`
3. ✅ Explore the other features in [NEW_FEATURES.md](NEW_FEATURES.md)
4. ✅ Check out the provider system in [KB_PROVIDERS.md](KB_PROVIDERS.md)

**Happy documenting! 🚀**

---

_If you found this guide helpful, consider giving the project a ⭐ on GitHub!_
