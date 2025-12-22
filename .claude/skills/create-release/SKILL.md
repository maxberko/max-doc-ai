---
name: create-release
description: Orchestrate complete product release workflow for FINISHED, PRODUCTION-READY features. Executes comprehensive release preparation including screenshot capture, documentation creation/updates, knowledge base sync, and customer announcement generation. ONLY invoke when user explicitly requests a "release", "launch", "announcement", or "release materials" for a completed feature ready for customer communication. Do NOT use for bug fixes, incomplete features, documentation-only updates, or internal changes. This is a high-stakes workflow that runs start-to-finish without stopping.
---

# Create Release

You are preparing a complete release for a new product feature. This includes creating customer announcements and updating product documentation.

**CRITICAL**: This skill has TWO phases:
1. **Interactive Pre-Flight** (START ONLY): Collect feature information, repository details, and release date via questions
2. **Automated Execution**: After information is collected, workflow runs COMPLETELY from start to finish WITHOUT STOPPING

Do NOT ask questions after the pre-flight phase. Do NOT pause for confirmation during automation.

## Pre-Flight Configuration (INTERACTIVE)

**THIS IS THE ONLY INTERACTIVE SECTION** - After completion, workflow runs fully automated.

### Important: Conversational Flow

**This skill uses a simple conversational approach - NO complex forms or multi-select options.**

The workflow:
1. Ask user to describe the feature (text response - can be name, description, or full PRD)
2. Ask where the code is located (text response - "current", folder path, or GitHub URL)
3. If GitHub URL provided: Check accessibility, ask for auth only if needed
4. Ask for release date (text response - "today" or any date format)
5. Show summary and confirm
6. Run automated workflow

Keep questions simple and accept flexible text responses.

### Step 1: Gather Feature Information

**IMPORTANT**: Start with a single, simple prompt. Do NOT present multiple choice options.

Use a regular text message (NOT AskUserQuestion tool) to ask:

```
Please describe the feature you're releasing. You can provide:
- A short sentence describing what was built
- Copy/paste a PRD (Product Requirements Document)
- Just the feature name (I'll research the codebase)
```

Wait for the user's response, then parse it:

**Parsing the response:**
```python
# Determine input type from user's text response
text = user_response.strip()
word_count = len(text.split())

if word_count > 50:
    FEATURE_INPUT_TYPE = "PRD"
    PRD_TEXT = text
elif word_count > 5:
    FEATURE_INPUT_TYPE = "Description"
    FEATURE_DESCRIPTION = text
else:
    FEATURE_INPUT_TYPE = "Name"
    FEATURE_NAME = text
```

**Question 2 - Repository Source:**

Use a regular text message to ask:

```
Where is the feature code located?
- Type "current" for this codebase
- Provide a folder path (e.g., /path/to/your/project or ./my-feature)
- Or paste a GitHub URL (e.g., https://github.com/username/repo)
```

**Processing the answer:**
```python
import os

response = user_response.strip()

if "github.com" in response.lower():
    # GitHub URL provided
    REPO_SOURCE = "External"
    GITHUB_REPO_URL = response
    # Will check accessibility and ask for auth if needed in Question 3
elif response.lower() in ["current", "here", "this repo", "this codebase"]:
    # Current codebase
    REPO_SOURCE = "Current"
    WORKING_DIR = os.getcwd()
elif os.path.exists(response) or response.startswith('./') or response.startswith('../') or response.startswith('/'):
    # Folder path provided
    REPO_SOURCE = "Local"
    WORKING_DIR = os.path.abspath(response)
    # Verify the path exists
    if not os.path.exists(WORKING_DIR):
        # Ask user to confirm the path or provide a different one
        print(f"⚠️ Warning: Path '{WORKING_DIR}' does not exist. Please provide a valid path.")
else:
    # Assume current codebase
    REPO_SOURCE = "Current"
    WORKING_DIR = os.getcwd()
```

**Question 3 - Authentication (conditional):**

**ONLY if a GitHub URL was provided in Question 2**, first check if the repository is accessible:

```python
import subprocess

# Try to check if repo is publicly accessible
try:
    result = subprocess.run(
        ["git", "ls-remote", GITHUB_REPO_URL],
        capture_output=True,
        timeout=10
    )
    if result.returncode == 0:
        # Repository is accessible (public or user already has auth configured)
        IS_PRIVATE_REPO = False
        AUTH_METHOD = None
        print(f"✅ GitHub repository is accessible: {GITHUB_REPO_URL}")
        # Skip to Question 4
    else:
        # Repository requires authentication
        IS_PRIVATE_REPO = True
        # Ask for authentication method
except Exception as e:
    # Assume private and ask for auth
    IS_PRIVATE_REPO = True
```

If repository is not accessible, use a regular text message to ask:

```
This repository requires authentication. How should I access it?
- Type "gh" to use GitHub CLI (if already authenticated)
- Type "ssh" to use SSH key
- Or paste your GitHub Personal Access Token (starts with ghp_ or github_pat_)
```

**Processing the answer:**
```python
response = user_response.strip()

if response.startswith("ghp_") or response.startswith("github_pat_"):
    # User pasted a GitHub PAT
    AUTH_METHOD = "Personal Access Token"
    GITHUB_PAT = response
elif response.lower() in ["gh", "github cli", "github-cli"]:
    AUTH_METHOD = "GitHub CLI"
elif response.lower() in ["ssh", "ssh key"]:
    AUTH_METHOD = "SSH"
else:
    # Default to GitHub CLI
    AUTH_METHOD = "GitHub CLI"
```

**Question 4 - Release Date:**

Use a regular text message to ask:

```
When was/will this feature be released?
- Type "today" for current date (2025-12-22)
- Or type a date (e.g., "2025-12-22" or "December 22, 2025")
```

**Processing the answer:**
```python
from datetime import datetime
import re

response = user_response.strip()

if response.lower() in ["today", "now"]:
    RELEASE_DATE = datetime.today().strftime('%Y-%m-%d')
else:
    # Parse date
    date_str = response

    # Try YYYY-MM-DD
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        RELEASE_DATE = date_str
    # Try MM/DD/YYYY
    elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        RELEASE_DATE = dt.strftime('%Y-%m-%d')
    # Try "Month DD, YYYY"
    else:
        try:
            dt = datetime.strptime(date_str, '%B %d, %Y')
            RELEASE_DATE = dt.strftime('%Y-%m-%d')
        except:
            # Default to today if parsing fails
            RELEASE_DATE = datetime.today().strftime('%Y-%m-%d')
```

### Step 2: Summary and Confirmation

After collecting all information, display a summary and ask for confirmation:

```
📋 Release Configuration Summary
================================

Feature Input: [PRD / Description / Name]
[Show first 100 chars if PRD/description provided]

Code Source:
  - Current codebase: [current working directory]
  OR
  - Local folder: [folder path]
  OR
  - GitHub repo: [repo URL]
    Auth: [Not needed / GitHub CLI / SSH / Personal Access Token]

Release Date: [YYYY-MM-DD]

Output Structure:
  Documentation: output/features/YYYY-MM-DD_feature-slug/
  Announcements: output/changelogs/YYYY-MM-DD/
  Screenshots: output/screenshots/

Proceed with this configuration? (Type "yes" to continue or "no" to restart)
```

Format the Code Source section based on `REPO_SOURCE`:
- If "Current": Show "Current codebase: [path]"
- If "Local": Show "Local folder: [WORKING_DIR]"
- If "External": Show "GitHub repo: [GITHUB_REPO_URL]" and auth method if applicable

Wait for user response. If they type anything other than "yes" or "y", restart the questions. Otherwise, continue to Step 3.

### Step 3: Prepare Working Directory

Handle working directory based on repository source:

**If GitHub URL was provided (REPO_SOURCE = "External"):**

Use bash commands to clone the repository:

```bash
# Create temp directory
REPO_NAME=$(basename "$GITHUB_REPO_URL" .git)
WORKING_DIR="/tmp/max-doc-ai-repos/$REPO_NAME"
mkdir -p "$WORKING_DIR"

# Clone based on authentication method
if [[ "$AUTH_METHOD" == "GitHub CLI" ]]; then
  gh repo clone "$GITHUB_REPO_URL" "$WORKING_DIR"
elif [[ "$AUTH_METHOD" == "SSH" ]]; then
  git clone "$GITHUB_REPO_URL" "$WORKING_DIR"
elif [[ "$AUTH_METHOD" == "Personal Access Token" ]]; then
  # Extract user/repo from URL
  REPO_PATH=$(echo "$GITHUB_REPO_URL" | sed 's|https://github.com/||' | sed 's|\.git||')
  git clone "https://${GITHUB_PAT}@github.com/${REPO_PATH}.git" "$WORKING_DIR"
else
  # No auth needed (public repo or already authenticated)
  git clone "$GITHUB_REPO_URL" "$WORKING_DIR"
fi

echo "✅ Repository cloned to: $WORKING_DIR"
```

**If local folder path was provided (REPO_SOURCE = "Local"):**

The `WORKING_DIR` was already set in Question 2 processing. Verify the path exists:

```bash
if [ -d "$WORKING_DIR" ]; then
  echo "✅ Using local directory: $WORKING_DIR"
else
  echo "❌ Error: Directory does not exist: $WORKING_DIR"
  exit 1
fi
```

**If current codebase was selected (REPO_SOURCE = "Current"):**

The `WORKING_DIR` is already set to the current working directory (`os.getcwd()`).

### Step 4: Create Feature Slug and Output Directories

Create a URL-safe slug from the feature name:

```python
import re
from datetime import datetime

# Get feature name
if FEATURE_INPUT_TYPE == "Feature name only":
    feature_name = FEATURE_NAME
elif FEATURE_INPUT_TYPE == "Short description":
    # Extract first few words from description
    feature_name = FEATURE_DESCRIPTION.split()[0:3]
    feature_name = " ".join(feature_name)
else:  # PRD
    # Try to extract feature name from PRD (look for title/heading)
    lines = PRD_TEXT.split('\n')
    feature_name = lines[0].strip('#').strip()

# Create slug
feature_slug = feature_name.lower()
feature_slug = re.sub(r'[^a-z0-9]+', '-', feature_slug)
feature_slug = feature_slug.strip('-')

print(f"Feature slug: {feature_slug}")

# Create output directories
import os

base_output = "./output"
features_dir = f"{base_output}/features/{RELEASE_DATE}_{feature_slug}"
changelogs_dir = f"{base_output}/changelogs/{RELEASE_DATE}"
screenshots_dir = f"{base_output}/screenshots"

for dir_path in [features_dir, changelogs_dir, screenshots_dir]:
    os.makedirs(dir_path, exist_ok=True)
    print(f"📁 Created: {dir_path}")
```

Store `feature_slug`, `features_dir`, `changelogs_dir`, and `screenshots_dir` for later use.

### End of Interactive Section

**From this point forward, the workflow proceeds fully automated using collected information.**

---

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

**Using Collected Context**

You now have feature context from the pre-flight phase:
- **Input type**: `FEATURE_INPUT_TYPE` (PRD, description, or name only)
- **Feature details**: `PRD_TEXT`, `FEATURE_DESCRIPTION`, or `FEATURE_NAME`
- **Working directory**: `WORKING_DIR` (current codebase or cloned external repo)
- **Release date**: `RELEASE_DATE`
- **Output directories**: `features_dir`, `changelogs_dir`, `screenshots_dir`

**Research Strategy Based on Input Type:**

- **If PRD provided**: You already understand the feature scope. Focus on:
  - Validating PRD claims against actual code implementation
  - Finding URLs/routes for screenshot capture
  - Identifying any implementation differences from the PRD

- **If description provided**: You have a summary. Focus on:
  - Expanding understanding with codebase exploration
  - Finding implementation details and technical specifics
  - Identifying configuration options and capabilities

- **If name only**: Full discovery mode. Focus on:
  - Understanding what was actually built
  - Discovering all capabilities and features
  - Identifying the problem it solves and target audience

**Research Process:**

Use `WORKING_DIR` as the base path for all file searches and exploration.

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
