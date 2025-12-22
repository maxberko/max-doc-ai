---
name: create-release
description: Orchestrate complete product release workflow for FINISHED, PRODUCTION-READY features. Executes comprehensive release preparation including screenshot capture, documentation creation/updates, knowledge base sync, and customer announcement generation. ONLY invoke when user explicitly requests a "release", "launch", "announcement", or "release materials" for a completed feature ready for customer communication. Do NOT use for bug fixes, incomplete features, documentation-only updates, or internal changes. This is a high-stakes workflow that runs start-to-finish without stopping.
---

# Create Release

You are preparing a complete release for a new product feature. This includes creating customer announcements and updating product documentation.

**CRITICAL**: This skill must run COMPLETELY from start to finish WITHOUT STOPPING. Do NOT ask the user questions unless absolutely critical. Do NOT pause for confirmation. Execute all steps sequentially until the entire release is complete.

## Input

The user will provide information about the feature being released. This can include:

1. **Feature name or description**: e.g., "Dashboard Analytics", "Workflow Automation", "Integration Hub"
2. **Feature description**: What was built and why
3. **PR numbers** (optional): Code changes that implement the feature
4. **Documentation category**: Which category this belongs to (features, integrations, getting-started)

## Overview

This skill orchestrates the complete release workflow:

1. **Capture screenshots** - FIRST
2. **Upload screenshots to Pylon** (get CloudFront URLs)
3. **Create/update product documentation** (with CloudFront image URLs)
4. **Sync to Pylon** (publish documentation with correct collection_id)
5. **Create customer announcements** (with Pylon article URL)
6. **Verify and report** (final summary with all URLs)

**CRITICAL ORDER**: Screenshots → Upload → Documentation (with images) → Pylon sync → Announcements (with article URL)

All tasks will research the codebase independently to understand the feature implementation.

**IMPORTANT**: Run all steps sequentially without stopping. Make reasonable assumptions based on codebase research. Only ask questions if the implementation is completely unclear or contradictory.

---

## Process

**Workflow**:
1. Research feature in codebase
2. Make reasonable inferences
3. Invoke `capture-screenshots` skill
4. Invoke `sync-docs` skill to upload screenshots to Pylon CDN
5. Invoke `update-product-doc` skill with CloudFront URLs
6. Invoke `sync-docs` skill again to publish documentation (get article URL)
7. Invoke `create-changelog` skill using Pylon article URL
8. Verify and create final summary

### Step 1: Research the Feature

Before doing anything, research the codebase to understand what was built:

1. **Identify the feature scope:**
   - Use the Task tool with `subagent_type=Explore` to find relevant code
   - Search for feature name in files, components, database schemas
   - Look in frontend, backend, API routes, database migrations

2. **Determine the feature category:**
   - Check config.yaml for available categories (default: getting-started, features, integrations)
   - Infer from codebase location and purpose

3. **Extract key information:**
   - Feature capabilities and user flows
   - Configuration options and settings
   - Dashboard views and navigation
   - Permissions and access control

4. **Identify target audience:**
   - Who will use this feature?
   - What problem does it solve?

**CRITICAL**: Do NOT ask the user for information. Make reasonable inferences from the codebase.

---

### Step 2: Make Inferences (NO QUESTIONS)

**DO NOT ASK THE USER QUESTIONS**. Instead, make reasonable inferences from your research:

- **Category**: Infer from feature type (features for general features, integrations for third-party integrations, getting-started for onboarding)
- **Target audience**: Infer from code location and capabilities
- **Value proposition**: Infer from feature capabilities and user benefits

If something is genuinely unclear, make the MOST REASONABLE assumption and document it in the summary. Do NOT stop to ask.

---

### Step 3: Capture Screenshots

Invoke the `capture-screenshots` skill:

```
Skill: capture-screenshots

Feature: [feature name]
Category: [category from config.yaml]
URLs to capture:
  - [list of URLs/pages to screenshot]

Please capture screenshots for this feature.
```

**Wait for screenshots to be captured before proceeding.**

---

### Step 4: Upload Screenshots to Pylon CDN

Invoke the `sync-docs` skill in upload mode:

```
Skill: sync-docs

Mode: upload-screenshots
Feature: [feature name]
Screenshots directory: [from config.yaml]

Please upload the screenshots to Pylon CDN and provide the CloudFront URLs.
```

**Save the CloudFront URLs** - you'll need them for the documentation.

---

### Step 5: Create/Update Documentation

Invoke the `update-product-doc` skill:

```
Skill: update-product-doc

Feature: [feature name]
Category: [category]
CloudFront URLs: [from step 4]

Create comprehensive documentation for this feature including:
- Overview and key capabilities
- Configuration instructions
- Use cases and examples
- Screenshots at appropriate sections

Use the CloudFront URLs for all screenshots.
```

**Wait for documentation to be written.**

---

### Step 6: Sync Documentation to Pylon

Invoke the `sync-docs` skill in sync mode:

```
Skill: sync-docs

Mode: sync-documentation
Feature: [feature name]
Category: [category]
Documentation file: [path to created .md file]

Please sync the documentation to Pylon knowledge base and provide the public article URL.
```

**Save the Pylon article URL** - you'll need it for announcements.

---

### Step 7: Create Customer Announcements

Invoke the `create-changelog` skill:

```
Skill: create-changelog

Feature: [feature name]
Documentation URL: [Pylon article URL from step 6]
Channels: [from config.yaml - e.g., slack, email]

Generate customer announcements for this feature release.
Include the Pylon documentation URL prominently.
```

**Wait for announcements to be generated.**

---

### Step 8: Verification and Final Summary

After all steps are complete, create a comprehensive summary:

```markdown
## 🚀 Release Complete: [Feature Name]

### ✅ Deliverables

**Screenshots:**
- Captured: [X] screenshots
- Location: [path]
- Uploaded to Pylon CDN: ✅

**Documentation:**
- File: [path to .md file]
- Pylon Article: [public URL]
- Collection: [category name]
- Screenshots: Embedded with CloudFront URLs

**Announcements:**
- Slack announcement: [path]
- Email announcement: [path]
- Documentation link: Included

### 📋 Summary

[Brief description of the feature and what was released]

**Key capabilities:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

**Target audience:** [Who this is for]

### 🔗 Links

- **Documentation:** [Pylon article URL]
- **Internal edit:** [Pylon internal URL if available]
- **Announcements:** [paths to generated files]

### ✅ Next Steps

1. Review the generated announcements
2. Schedule announcement distribution
3. Monitor customer feedback
4. Update documentation based on feedback

---

*🤖 Generated with max-doc-AI - Complete release automation*
```

---

## Important Notes

### Configuration Requirements

Ensure these are properly set in `config.yaml`:

```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"

pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
    integrations: "${COLLECTION_INTEGRATIONS_ID}"

documentation:
  base_path: "./demo/docs/product_documentation"
  categories:
    - getting-started
    - features
    - integrations

announcements:
  output_dir: "./demo/docs/product_documentation/changelog"
  channels:
    - slack
    - email
```

### Error Handling

If any step fails:
1. Document the failure clearly
2. Complete remaining steps if possible
3. Provide clear instructions for manual completion
4. Do NOT stop the entire workflow for minor issues

### Success Criteria

✅ All screenshots captured and uploaded
✅ Documentation created/updated with embedded images
✅ Documentation synced to Pylon with correct collection
✅ Announcements generated with documentation URL
✅ All URLs and paths verified and working

---

## Troubleshooting

**Screenshots fail:**
- Check if authentication session exists
- Verify URLs in config.yaml
- Try running auth_manager.py

**Pylon upload fails:**
- Verify PYLON_API_KEY is set
- Check network connectivity
- Verify image files exist

**Documentation sync fails:**
- Verify collection IDs in config.yaml
- Check PYLON_KB_ID is correct
- Ensure markdown is valid

**Announcements incomplete:**
- Verify announcement channels in config.yaml
- Check template structure
- Ensure documentation URL is available
