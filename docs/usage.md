# Usage Guide

How to use max-doc-AI with Claude Code.

## Overview

max-doc-AI provides 5 Claude skills that work together to automate your documentation workflow:

1. **create-release** - Master orchestrator (runs all others)
2. **capture-screenshots** - Capture product screenshots
3. **update-product-doc** - Write/update documentation
4. **sync-docs** - Upload screenshots & sync to Pylon
5. **create-changelog** - Generate customer announcements

## Quick Start: Complete Release

The simplest way to create a complete release:

```
@claude Create a release for the Dashboards feature
```

Claude will:
1. Research the feature in your codebase
2. Capture screenshots
3. Upload to Pylon CDN
4. Create documentation
5. Sync to Pylon
6. Generate announcements

**Requirements:**
- Feature code exists in your codebase
- Authentication session saved (`auth_manager.py`)
- Configuration complete

## Individual Skills

### Capture Screenshots

```
@claude Skill: capture-screenshots

Feature: Dashboards
Category: features
URLs to capture:
- /dashboards (overview)
- /dashboards/customize (settings)
```

**Creates:** Screenshot files in `screenshots/` directory

### Update Documentation

```
@claude Skill: update-product-doc

Feature: Dashboards
Category: features
CloudFront URLs: [from previous step]

Create comprehensive documentation with these screenshots.
```

**Creates:** Markdown file in `demo/docs/product_documentation/[category]/`

### Sync to Pylon

**Mode 1 - Upload Screenshots:**
```
@claude Skill: sync-docs

Mode: upload-screenshots
Feature: Dashboards

Upload screenshots to Pylon CDN and provide CloudFront URLs.
```

**Mode 2 - Sync Documentation:**
```
@claude Skill: sync-docs

Mode: sync-documentation
Feature: Dashboards
Category: features
File: demo/docs/product_documentation/features/dashboards.md

Sync to Pylon KB and provide public URL.
```

### Create Announcements

```
@claude Skill: create-changelog

Feature: Dashboards
Documentation URL: [Pylon public URL]
Channels: slack, email

Generate customer announcements.
```

**Creates:** Announcement files in `changelog/[feature]/`

## Workflow Best Practices

### Before Starting

1. ✅ Feature is complete and tested
2. ✅ Authentication session is saved
3. ✅ Configuration is correct
4. ✅ Pylon collections exist

### During Execution

- Let Claude run without interruption
- Review generated content
- Verify screenshots captured correctly
- Check Pylon URLs are accessible

### After Completion

1. Review all generated files
2. Test Pylon article links
3. Customize announcements if needed
4. Schedule release communication
5. Monitor customer feedback

## Common Workflows

### New Feature Release

**Full automation:**
```
@claude Create a release for [Feature Name]
```

### Update Existing Documentation

**Just update docs:**
```
@claude Skill: update-product-doc

Feature: [Feature Name]
Category: [category]

Update the documentation to add [new information].
```

Then sync:
```
@claude Skill: sync-docs

Mode: sync-documentation
Feature: [Feature Name]
Category: [category]
File: [path to .md file]
```

### Add New Screenshots

**Capture and upload:**
```
@claude Skill: capture-screenshots
Feature: [Feature Name]
URLs: [new URLs to capture]
```

```
@claude Skill: sync-docs
Mode: upload-screenshots
Feature: [Feature Name]
```

Then update documentation with new CloudFront URLs.

### Announcements Only

If docs already exist:
```
@claude Skill: create-changelog
Feature: [Feature Name]
Documentation URL: [existing Pylon URL]
```

## Tips & Tricks

**Let Claude Research:**
Claude explores your codebase to understand features. Give it time.

**Be Specific:**
Provide feature names, categories, and any special context.

**Check State:**
```bash
python3 scripts/utils/state.py --summary
```
Shows what's synced to Pylon.

**Re-run Steps:**
Skills are idempotent - safe to re-run if something fails.

**Test Screenshots:**
Run `capture-screenshots` first to verify auth and URLs work.

## Troubleshooting

See individual skill documentation in `.claude/skills/` for detailed troubleshooting.

**Common issues:**

- **Screenshots blank**: Re-run `auth_manager.py`
- **Pylon 401 error**: Check API key in `.env`
- **Skills can't find feature**: Provide more context about code location
- **Images not in Pylon**: Check CloudFront URLs are valid

## Advanced Usage

### Custom Screenshot Scripts

Create your own in `scripts/screenshot/`:

```python
from screenshot.capture import ScreenshotCapturer
import config as cfg

with ScreenshotCapturer() as capturer:
    capturer.navigate('https://your-url.com')
    capturer.capture('screenshot-name')
```

### Batch Operations

Sync multiple articles:
```python
from pylon.sync import sync_documentation_category

articles = [
    {'key': 'feature-1', 'file': 'features/feature-1.md', ...},
    {'key': 'feature-2', 'file': 'features/feature-2.md', ...}
]

sync_documentation_category('features', articles)
```

### Custom Announcement Templates

Edit generated announcements before distribution. They're just markdown files in `changelog/`.

## Next Steps

- Read [Configuration Guide](configuration.md) for all options
- Check [Pylon Integration](pylon-integration.md) for API details
- Review [Demo Product](demo-product.md) for examples
