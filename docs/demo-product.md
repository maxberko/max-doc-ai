# Demo Product: FlowState

Example documentation workflow demonstrating max-doc-AI's capabilities.

## Overview

The `demo/` directory contains complete example documentation for **FlowState**, a fictional workflow automation platform. This demonstrates the full max-doc-AI workflow from feature implementation to customer announcements.

**FlowState** is used as a realistic example to showcase:
- Feature documentation structure
- Screenshot integration
- Multi-channel announcements
- Knowledge base organization
- Complete release materials

## Demo Contents

### Product Documentation

Located in `demo/docs/product_documentation/`:

```
demo/docs/product_documentation/
├── getting-started/
│   └── quickstart.md           # New user onboarding
├── features/
│   ├── dashboards.md           # Dashboard feature (complete example)
│   ├── automation.md           # Automation capabilities
│   └── integrations.md         # Integration guides
├── screenshots/                # Product screenshots
│   └── *.png
└── changelog/
    └── dashboards/             # Release materials for Dashboards
        ├── README.md           # Changelog overview
        ├── slack-announcement.md
        └── email-announcement.md
```

### Documentation Categories

**Getting Started** (`getting-started/`)
- Quickstart guide for new users
- Initial setup and first workflow
- Basic concepts and terminology

**Features** (`features/`)
- Core feature documentation
- Dashboards (full example)
- Automation workflows
- Integration capabilities

**Integrations** (`integrations/`)
- Third-party integration guides
- API documentation
- Webhook configurations

### Changelog & Announcements

Located in `demo/docs/product_documentation/changelog/`:

Each feature release gets its own directory containing:
- **README.md** - Changelog entry summary
- **slack-announcement.md** - Short, engaging Slack post
- **email-announcement.md** - Detailed email announcement

## Example: Dashboards Feature

The **Dashboards** feature is a complete example showing the full workflow.

### 1. Feature Documentation

**File:** `demo/docs/product_documentation/features/dashboards.md`

**Contains:**
- Feature overview and key capabilities
- How-to guides with screenshots
- Configuration options
- Multiple use cases
- FAQ section
- Best practices

**Structure:**
```markdown
# Dashboards

## Overview
[High-level description]

## Key Capabilities
[What it does]

## How It Works
[Step-by-step guides with screenshots]

## Configuration
[Settings and options]

## Use Cases
[Real-world examples]

## FAQ
[Common questions]

## Best Practices
[Tips for success]
```

### 2. Screenshots

**Files:** `demo/docs/product_documentation/screenshots/`
- `dashboards-overview.png` - Main dashboard view
- `dashboards-customization.png` - Widget configuration
- `dashboards-widgets.png` - Available widget types
- `dashboards-layout.png` - Drag-and-drop layout
- `dashboards-share.png` - Sharing interface

**Placeholder URLs:**
```markdown
![Dashboard overview](https://placeholder-cloudfront-url.com/dashboards-overview.png)
```

*In production, these would be replaced with actual CloudFront URLs from Pylon CDN.*

### 3. Customer Announcements

**Slack Announcement** (`changelog/dashboards/slack-announcement.md`):
- Short, engaging format
- Emojis for visual interest
- Key benefits highlighted
- Link to documentation
- Call to action

**Email Announcement** (`changelog/dashboards/email-announcement.md`):
- Longer, detailed format
- Feature benefits explained
- Multiple use cases
- Visual sections
- Documentation links
- Support information

### 4. Changelog Entry

**Changelog** (`changelog/dashboards/README.md`):
- Release date
- Feature summary
- Key improvements
- Links to documentation
- Links to announcements

## Workflow Demonstration

### How This Demo Was Created

This demonstrates the full max-doc-AI workflow:

#### Step 1: Feature Implementation
```
# Fictional: Dashboards feature implemented in FlowState codebase
# In real usage, Claude would research your actual codebase
```

#### Step 2: Capture Screenshots
```
@claude Skill: capture-screenshots

Feature: Dashboards
Category: features
URLs to capture:
- /dashboards (overview)
- /dashboards/customize (customization)
- /dashboards/widgets (available widgets)
- /dashboards/layout (drag-and-drop)
- /dashboards/share (sharing interface)
```

**Result:** 5 screenshots saved to `screenshots/` directory

#### Step 3: Upload to Pylon CDN
```
@claude Skill: sync-docs

Mode: upload-screenshots
Feature: Dashboards

Upload all dashboard screenshots to Pylon CDN.
```

**Result:** CloudFront URLs returned for each screenshot

#### Step 4: Create Documentation
```
@claude Skill: update-product-doc

Feature: Dashboards
Category: features
CloudFront URLs: [URLs from Step 3]

Create comprehensive documentation for the Dashboards feature.
```

**Result:** `features/dashboards.md` created with embedded screenshots

#### Step 5: Sync to Pylon KB
```
@claude Skill: sync-docs

Mode: sync-documentation
Feature: Dashboards
Category: features
File: demo/docs/product_documentation/features/dashboards.md

Sync to Pylon Knowledge Base.
```

**Result:** Article created in Pylon with public URL

#### Step 6: Generate Announcements
```
@claude Skill: create-changelog

Feature: Dashboards
Documentation URL: [Pylon public URL from Step 5]
Channels: slack, email

Generate customer announcements.
```

**Result:**
- `changelog/dashboards/slack-announcement.md`
- `changelog/dashboards/email-announcement.md`
- `changelog/dashboards/README.md`

### Complete Release (All in One)

Or use the orchestrator skill to do everything at once:

```
@claude Skill: create-release

Feature: Dashboards

Create complete release materials: screenshots, documentation, Pylon sync, and announcements.
```

**Result:** All of the above in one automated workflow

## Using the Demo

### 1. Explore the Files

Browse the demo documentation to see:
- How documentation is structured
- What level of detail is included
- How screenshots are embedded
- Announcement formats and tone

### 2. Customize for Your Product

Replace FlowState with your product:

**Update config.yaml:**
```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
  documentation_url: "https://docs.yourproduct.com"
```

**Update file paths:**
- Keep the same directory structure
- Replace FlowState content with your features
- Maintain the same documentation patterns

### 3. Generate Your Own Documentation

Follow the same workflow for your features:

1. Implement a feature in your codebase
2. Run `capture-screenshots` with your product URLs
3. Upload screenshots to Pylon
4. Generate documentation from your codebase
5. Sync to your Pylon KB
6. Create announcements for your channels

### 4. Compare Outputs

Use the demo as a reference:
- Does your documentation have similar depth?
- Are screenshots clear and professional?
- Do announcements follow the right tone?
- Is information well-organized?

## Demo Files Explained

### Quickstart Guide

**Purpose:** Help new users get started quickly

**Key sections:**
- What you'll learn
- Prerequisites
- Step-by-step tutorial (6 steps)
- Next steps
- Common use cases
- Tips for success

**Pattern:** Progressive disclosure - basic first, then advanced

### Feature Documentation (Dashboards)

**Purpose:** Comprehensive reference for a feature

**Key sections:**
- Overview and value proposition
- Key capabilities (bulleted)
- How it works (with screenshots)
- Configuration options (table format)
- Use cases (4 real-world examples)
- FAQ (6 common questions)
- Best practices (8 tips)

**Pattern:** Task-oriented with visual guidance

### Announcements

**Slack Format:**
- 📊 Opening with emoji
- 2-3 sentence hook
- 3 key benefits (bullets)
- Documentation link
- Friendly call to action

**Email Format:**
- Compelling subject line
- Feature introduction
- Detailed benefits
- Use case examples
- Visual sections with headers
- Multiple CTAs
- Support information

**Pattern:** Slack = scannable, Email = comprehensive

## Customization Tips

### Adapting the Structure

**Keep:**
- Directory structure (`getting-started/`, `features/`, etc.)
- Documentation patterns (Overview, How It Works, Use Cases)
- Announcement formats (Slack vs Email approaches)

**Customize:**
- Category names (match your product domains)
- Section order (based on user journey)
- Use case specifics (your customer scenarios)
- Tone and voice (match your brand)

### Adding New Categories

1. Create directory: `demo/docs/product_documentation/new-category/`
2. Add to `config.yaml`:
   ```yaml
   documentation:
     categories:
       - getting-started
       - features
       - integrations
       - new-category  # Add here
   ```
3. Create Pylon collection
4. Add collection ID to `.env`
5. Update `config.yaml` with collection mapping

### Templating Your Own Content

**Create templates based on the demo:**

**Feature Template** (based on `dashboards.md`):
```markdown
# [Feature Name]

## Overview
[Value proposition]

## Key Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

## How It Works
[Step-by-step with screenshots]

## Configuration
[Settings table]

## Use Cases
### Use Case 1: [Name]
**Situation:** [Problem]
**Solution:** [How feature helps]
**Example:** [Real scenario]

## FAQ
**Q: [Question]**
A: [Answer]

## Best Practices
1. [Tip 1]
2. [Tip 2]
```

## Best Practices from the Demo

### Documentation Structure

1. **Start with value** - Lead with "why should I care?"
2. **Show, don't tell** - Use screenshots liberally
3. **Multiple learning styles** - Text, images, examples
4. **Progressive complexity** - Simple concepts first
5. **Practical examples** - Real use cases, not theory

### Screenshot Strategy

1. **Consistent viewport** - All screenshots same size (1470x840)
2. **Highlight key areas** - Draw attention to important UI
3. **Show workflows** - Capture multi-step processes
4. **Clean test data** - Professional example content
5. **Accessible alt text** - Describe what's shown

### Announcement Approach

1. **Know your channel** - Slack ≠ Email ≠ In-app
2. **Hook quickly** - First sentence matters
3. **Benefits over features** - "Save time" not "New button"
4. **Clear CTAs** - Tell users what to do next
5. **Link generously** - Documentation, tutorials, support

## Technical Details

### File Paths

All demo files use relative paths from project root:
```
./demo/docs/product_documentation/[category]/[feature].md
```

### Screenshot References

Placeholder URLs in demo files:
```markdown
![Alt text](https://placeholder-cloudfront-url.com/filename.png)
```

In production, these are replaced with actual CloudFront URLs:
```markdown
![Alt text](https://d1234567.cloudfront.net/filename.png)
```

### State Tracking

Demo articles recorded in `demo/docs/sync-state.json`:
```json
{
  "articles": {
    "features/dashboards": {
      "pylon_article_id": "...",
      "url": "...",
      "synced_at": "..."
    }
  }
}
```

## Next Steps

1. **Study the demo files** to understand the documentation patterns
2. **Run the workflow** on your own features
3. **Compare outputs** to the demo quality
4. **Iterate and improve** based on what works
5. **Build your library** of documentation and announcements

## Resources

**Demo Files:**
- [Quickstart Guide](../demo/docs/product_documentation/getting-started/quickstart.md)
- [Dashboards Feature](../demo/docs/product_documentation/features/dashboards.md)
- [Slack Announcement](../demo/docs/product_documentation/changelog/dashboards/slack-announcement.md)
- [Email Announcement](../demo/docs/product_documentation/changelog/dashboards/email-announcement.md)

**Related Guides:**
- [Usage Guide](usage.md) - How to run the workflow
- [Setup Guide](setup.md) - Configure for your product
- [Configuration Reference](configuration.md) - All options

---

**The FlowState demo shows what's possible with max-doc-AI.** Use it as inspiration for your own product documentation workflow.
