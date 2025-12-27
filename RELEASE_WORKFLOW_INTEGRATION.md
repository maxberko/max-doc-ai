# Release Workflow Integration with Documentation Discovery

This document explains how the documentation discovery system integrates with the `create-release` workflow.

## Overview

The create-release workflow now has **awareness** of existing documentation at every step:

```
1. Pre-Flight     → Check if docs already exist
2. Research       → Understand codebase
3. Classify       → Determine if screenshots needed
4. Screenshots    → Capture if needed
5. Upload         → Upload to KB CDN
6. Documentation  → ✅ CHECK: Does doc exist? Update or create?
7. Sync to KB     → ✅ DISCOVER: What will be synced?
                  → ✅ VERIFY: Did sync succeed?
8. Announcements  → Generate with doc URLs
9. Summary        → ✅ SHOW: Full inventory of what was created
```

## Integration Points

### 1. **Pre-Flight: Check Existing Documentation**

**When:** Before starting the release workflow
**Why:** Know if you're updating existing docs or creating new ones

```python
# At the start of create-release, after gathering feature info:

from utils.doc_inventory import DocumentInventory

# Scan existing documentation
inventory = DocumentInventory()
inventory.scan()

# Check if documentation already exists for this feature
feature_slug = "dashboards"  # Derived from feature name
existing_docs = [
    doc for doc in inventory.documents
    if doc.slug == feature_slug and doc.category in ['features', 'getting-started']
]

if existing_docs:
    print(f"📝 Found {len(existing_docs)} existing document(s) for '{feature_slug}'")
    for doc in existing_docs:
        print(f"   • {doc.path}")
        print(f"     Category: {doc.category}")
        if doc.synced:
            print(f"     ✅ Already synced to {doc.sync_provider}")
            print(f"     URL: {doc.public_url}")
        else:
            print(f"     ⏳ Not synced yet")

    print("\n💡 This release will UPDATE existing documentation")
else:
    print(f"📄 No existing documentation found for '{feature_slug}'")
    print("💡 This release will CREATE new documentation")
```

**Output Example:**
```
📝 Found 1 existing document(s) for 'dashboards'
   • ./demo/docs/product_documentation/features/dashboards.md
     Category: features
     ✅ Already synced to pylon
     URL: https://yourproduct-kb.help.usepylon.com/articles/dashboards

💡 This release will UPDATE existing documentation
```

### 2. **After Documentation Creation: Verify What Was Created**

**When:** After `update-product-doc` skill completes
**Why:** Confirm documentation was created/updated successfully

```python
# After documentation is written:

# Re-scan to see what changed
inventory_after = DocumentInventory()
inventory_after.scan()

# Find the newly created/updated docs
new_docs = inventory_after.filter_by_category('features')

print("\n📄 Documentation Created/Updated:")
print("=" * 70)

for doc in new_docs:
    if doc.feature_date == RELEASE_DATE and doc.slug == feature_slug:
        print(f"✅ {doc.title}")
        print(f"   Path: {doc.path}")
        print(f"   Category: {doc.category}")
        print(f"   Size: {doc.size_bytes:,} bytes")
        print(f"   Status: {'Synced' if doc.synced else 'Ready to sync'}")
        print()
```

**Output Example:**
```
📄 Documentation Created/Updated:
======================================================================
✅ Dashboards
   Path: /Users/max/output/features/2025-12-25_dashboards/dashboards.md
   Category: features
   Size: 12,458 bytes
   Status: Ready to sync
```

### 3. **Before Sync: Preview What Will Be Synced**

**When:** Before invoking `sync-docs` skill
**Why:** Show exactly what will be synced and where

```python
# Before syncing:

print("\n🔄 Preparing to Sync Documentation")
print("=" * 70)

# Show what will be synced
doc_to_sync = {
    'file': f'output/features/{RELEASE_DATE}_{feature_slug}/{feature_slug}.md',
    'key': f'features-{feature_slug}',
    'title': feature_title,
    'slug': feature_slug,
    'collection': 'features',
    'provider': kb_provider  # From config
}

print(f"Provider: {doc_to_sync['provider']}")
print(f"Collection: {doc_to_sync['collection']}")
print(f"Title: {doc_to_sync['title']}")
print(f"Slug: {doc_to_sync['slug']}")
print(f"File: {doc_to_sync['file']}")

# Check if this will be create or update
state_key = f"{doc_to_sync['provider']}:{doc_to_sync['key']}"
state_data = state_manager.load_state()
existing = state_data.get('articles', {}).get(state_key)

if existing:
    print(f"\n💡 Action: UPDATE existing article")
    print(f"   Current URL: {existing.get('public_url')}")
else:
    print(f"\n💡 Action: CREATE new article")

print("\n🚀 Invoking sync-docs skill...")
```

**Output Example:**
```
🔄 Preparing to Sync Documentation
======================================================================
Provider: pylon
Collection: features
Title: Dashboards
Slug: dashboards
File: output/features/2025-12-25_dashboards/dashboards.md

💡 Action: CREATE new article

🚀 Invoking sync-docs skill...
```

### 4. **After Sync: Verify Success**

**When:** After `sync-docs` skill completes
**Why:** Confirm sync succeeded and get URLs for announcements

```python
# After sync-docs completes:

# Re-scan to check sync status
inventory_final = DocumentInventory()
inventory_final.scan()

# Find the synced document
synced_doc = next(
    (doc for doc in inventory_final.documents
     if doc.slug == feature_slug and doc.category == 'features'),
    None
)

if synced_doc and synced_doc.synced:
    print("\n✅ Documentation Synced Successfully!")
    print("=" * 70)
    print(f"Title: {synced_doc.title}")
    print(f"Provider: {synced_doc.sync_provider}")
    print(f"Synced: {synced_doc.sync_date}")
    print(f"\n🌐 Public URL (use in announcements):")
    print(f"   {synced_doc.public_url}")

    # Save for announcement step
    DOCUMENTATION_URL = synced_doc.public_url
else:
    print("\n❌ Sync verification failed!")
    print("   Documentation may not have synced successfully")
    print("   Run: python3 scripts/kb/sync.py status")
```

**Output Example:**
```
✅ Documentation Synced Successfully!
======================================================================
Title: Dashboards
Provider: pylon
Synced: 2025-12-25T16:30:45

🌐 Public URL (use in announcements):
   https://yourproduct-kb.help.usepylon.com/articles/dashboards
```

### 5. **Final Summary: Complete Release Inventory**

**When:** End of release workflow
**Why:** Show everything that was created and where it is

```python
# At the end of create-release:

print("\n" + "=" * 70)
print("📊 Release Summary")
print("=" * 70)

# Show all artifacts created
inventory_final = DocumentInventory()
inventory_final.scan()

# Filter to this release
release_docs = [
    doc for doc in inventory_final.documents
    if doc.feature_date == RELEASE_DATE
]

print(f"\n📦 Artifacts Created for {feature_title}")
print(f"   Release Date: {RELEASE_DATE}")
print(f"   Feature Slug: {feature_slug}")

print(f"\n📄 Documentation:")
for doc in release_docs:
    if doc.category == 'features':
        print(f"   • {doc.title}")
        print(f"     Path: {doc.path}")
        if doc.synced:
            print(f"     ✅ Synced: {doc.public_url}")
        else:
            print(f"     ⏳ Not synced")

print(f"\n📣 Announcements:")
announcement_docs = [d for d in release_docs if d.category == 'changelog']
for doc in announcement_docs:
    print(f"   • {doc.filename}")
    print(f"     Path: {doc.path}")

print(f"\n🖼️  Screenshots:")
screenshots_dir = f"output/screenshots/"
if os.path.exists(screenshots_dir):
    screenshots = [f for f in os.listdir(screenshots_dir)
                   if feature_slug in f and f.endswith('.png')]
    print(f"   {len(screenshots)} screenshot(s) in {screenshots_dir}")
    for screenshot in screenshots[:5]:  # Show first 5
        print(f"     • {screenshot}")
    if len(screenshots) > 5:
        print(f"     ... and {len(screenshots) - 5} more")

print("\n" + "=" * 70)
```

**Output Example:**
```
======================================================================
📊 Release Summary
======================================================================

📦 Artifacts Created for Dashboards
   Release Date: 2025-12-25
   Feature Slug: dashboards

📄 Documentation:
   • Dashboards
     Path: output/features/2025-12-25_dashboards/dashboards.md
     ✅ Synced: https://yourproduct-kb.help.usepylon.com/articles/dashboards

📣 Announcements:
   • email-us-en.md
     Path: output/changelogs/2025-12-25/dashboards/email-us-en.md
   • slack-us-en.md
     Path: output/changelogs/2025-12-25/dashboards/slack-us-en.md
   • email-eu-fr.md
     Path: output/changelogs/2025-12-25/dashboards/email-eu-fr.md
   ... (6 total)

🖼️  Screenshots:
   5 screenshot(s) in output/screenshots/
     • dashboards-overview.png
     • dashboards-widgets.png
     • dashboards-customization.png
     • dashboards-sharing.png
     • dashboards-exports.png

======================================================================
```

## Usage Commands During Release

### Check Status Anytime

```bash
# See what documentation exists and sync status
python3 scripts/kb/sync.py status

# Discover all documentation (with sync commands)
python3 scripts/kb/sync.py discover

# Export inventory to JSON
python3 utils/doc_inventory.py --export inventory.json
```

### Manual Sync If Needed

If automatic sync fails during release:

```bash
# Sync a specific document
python3 scripts/kb/sync.py sync \
  --file output/features/2025-12-25_dashboards/dashboards.md \
  --key features-dashboards \
  --title "Dashboards" \
  --slug "dashboards" \
  --collection features
```

### Verify After Release

```bash
# Show only synced documentation
python3 utils/doc_inventory.py --synced

# Show only unsynced documentation
python3 utils/doc_inventory.py --unsynced

# Show details for specific category
python3 utils/doc_inventory.py --category features --details
```

## Benefits

### 1. **No More Blind Operations**

**Before:**
```
Creating documentation...
✅ Done!

(Did it work? Where is it? Was it synced?)
```

**After:**
```
📝 Found 1 existing document for 'dashboards'
   • Already synced to pylon
   • URL: https://...
💡 This release will UPDATE existing documentation

✅ Documentation created: dashboards.md (12,458 bytes)
✅ Synced successfully to pylon
🌐 Public URL: https://...

Use this URL in announcements ✅
```

### 2. **Automatic Error Detection**

The system catches:
- ❌ Documentation created but not synced
- ❌ Sync claimed success but state not updated
- ❌ Wrong collection/category assigned
- ❌ Missing files after creation

### 3. **Clear Action Items**

If something isn't synced, you get exact commands:

```
⏳ Not synced: dashboards.md

To sync:
python3 scripts/kb/sync.py sync \
  --file output/features/2025-12-25_dashboards/dashboards.md \
  --key features-dashboards \
  --title "Dashboards" \
  --slug "dashboards" \
  --collection features
```

### 4. **Confidence in Release**

Before announcing:
```bash
python3 scripts/kb/sync.py status
```

Confirms:
- ✅ All documentation is synced
- ✅ Public URLs are available
- ✅ Screenshots are uploaded
- ✅ Ready to announce!

## Implementation in create-release Skill

The `create-release` skill should call these at key points:

```python
# Import at top of skill
from utils.doc_inventory import DocumentInventory, scan_documentation

# 1. Pre-Flight: Check existing
inventory = DocumentInventory()
docs = inventory.scan()
# ... show what exists ...

# 2. After doc creation: Verify
inventory.scan()  # Re-scan
# ... show what was created ...

# 3. Before sync: Preview
# ... show what will be synced ...

# 4. After sync: Verify
inventory.scan()  # Re-scan again
# ... verify sync succeeded ...

# 5. Final: Summary
inventory.print_summary()
# ... show complete inventory ...
```

## Future Enhancements

- **Diff detection**: Show exactly what changed in updated docs
- **Version tracking**: Track documentation versions over time
- **Bulk sync**: Sync multiple docs in one command
- **Provider comparison**: Compare same doc across multiple providers

---

**The key insight:** The release workflow now knows what documentation exists, where it is, and whether it's synced - at every step of the process.
