---
name: update-product-doc
description: Create or update product documentation in markdown format. Researches codebase to understand feature implementation, generates comprehensive documentation including overview, configuration, use cases, and embeds screenshots using provided CloudFront URLs. Follows established documentation patterns and structure.
---

# Update Product Documentation

Create or update comprehensive product documentation for features.

## Purpose

Generate professional, user-focused documentation that explains features clearly and includes visual aids (screenshots). Documentation is written in markdown and later synced to the Pylon knowledge base.

## Input

The user will provide:

1. **Feature name**: e.g., "Dashboards", "Workflow Automation"
2. **Category**: Documentation category (features, integrations, getting-started)
3. **CloudFront URLs**: Screenshot URLs from Pylon CDN (optional if updating existing)
4. **Optional context**: Specific aspects to cover, target audience

## Process

### Step 1: Research Feature Implementation

Use the Task tool with `subagent_type=Explore` to understand the feature:

**What to find:**

1. **Core Functionality:**
   - What does this feature do?
   - What problem does it solve?
   - Who is it for?

2. **User Flows:**
   - How do users access it?
   - What are the main workflows?
   - What actions can users take?

3. **Configuration:**
   - Are there settings or options?
   - What can be customized?
   - What are the defaults?

4. **Permissions & Access:**
   - Who can use this?
   - Are there role-based restrictions?
   - Any prerequisites?

5. **Integration Points:**
   - Does it connect to other features?
   - External integrations?
   - Data sources?

**Example:**
```
Task: Explore

Research the [Feature Name] feature implementation.

Please find:
1. Route/page components
2. Main functionality and user flows
3. Configuration options and settings
4. Database schema if relevant
5. Key capabilities and use cases

Focus on user-facing aspects, not internal implementation details.
```

### Step 2: Determine Documentation Structure

Based on your research, plan the documentation structure:

**Standard Structure:**

```markdown
# [Feature Name]

## Overview
- Brief introduction (2-3 sentences)
- Key benefits
- Who should use this
- Link to product (if applicable)

## Key Capabilities
- Capability 1: Description
- Capability 2: Description
- Capability 3: Description

## How It Works
- Step-by-step explanation
- Include screenshots at relevant points
- User perspective (not technical implementation)

## Configuration
- How to set it up
- Available options
- Best practices

## Use Cases
- Real-world scenarios
- Examples of how to use effectively

## FAQ
- Common questions
- Troubleshooting tips (basic only)

## Need Help?
- Support contact information
```

**Note:** Adjust structure based on feature type. Some sections may not be applicable.

### Step 3: Write Documentation

Write clear, user-focused documentation:

**Writing Guidelines:**

1. **Start with H2, not H1**: Pylon displays the title separately, so begin with ## Overview

2. **User-focused language:**
   - ✅ "You can customize your dashboard by..."
   - ❌ "The dashboard component implements..."

3. **Clear and concise:**
   - Short paragraphs (2-4 sentences)
   - Bullet points for lists
   - Active voice

4. **Embed screenshots:**
   ```markdown
   ![Dashboard overview](https://cloudfront.url/dashboard-overview.png)

   The main dashboard shows real-time metrics...
   ```

5. **Include console/app URLs** (if applicable):
   ```markdown
   Access dashboards at: `https://app.yourproduct.com/dashboards`
   ```

6. **No H1 heading:** Start directly with H2 sections

**Example Documentation:**

```markdown
## Overview

[Feature Name] helps teams [solve problem] by [key benefit]. With [Feature Name], you can [main capabilities in one sentence].

Access [Feature Name] at: `https://app.yourproduct.com/[feature-path]`

## Key Capabilities

- **[Capability 1]**: [Brief description of what it does and why it's useful]
- **[Capability 2]**: [Brief description]
- **[Capability 3]**: [Brief description]

## How It Works

### Accessing [Feature Name]

![Feature overview](https://cloudfront.url/feature-overview.png)

Navigate to [Feature Name] from the main menu. You'll see [what they see].

### [Main User Flow 1]

![Feature flow](https://cloudfront.url/feature-flow.png)

To [accomplish task]:

1. Click [button/link]
2. [Action 2]
3. [Action 3]

### [Main User Flow 2]

![Another view](https://cloudfront.url/feature-detail.png)

[Description of this workflow]

## Configuration

### Basic Setup

To configure [Feature Name]:

1. Go to Settings
2. Navigate to [Section]
3. Configure [options]

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| [Option 1] | [What it does] | [Default value] |
| [Option 2] | [What it does] | [Default value] |

### Best Practices

- **[Practice 1]**: [Why this is recommended]
- **[Practice 2]**: [Why this is recommended]

## Use Cases

### Use Case 1: [Scenario Name]

**Situation:** [Describe the scenario]

**Solution:** [How this feature helps]

**Example:** [Concrete example]

### Use Case 2: [Scenario Name]

[Same structure]

## FAQ

**Q: [Common question]?**

A: [Clear answer]

**Q: [Another question]?**

A: [Clear answer]

## Need Help?

If you have questions or need assistance:
- Visit our [Help Center](https://docs.yourproduct.com)
- Contact support: support@yourproduct.com
```

### Step 4: Save Documentation File

Save the documentation to the correct location:

**File path:**
```
demo/docs/product_documentation/[category]/[feature-slug].md
```

**Examples:**
- `demo/docs/product_documentation/features/dashboards.md`
- `demo/docs/product_documentation/integrations/slack-integration.md`
- `demo/docs/product_documentation/getting-started/quickstart.md`

**Filename convention:**
- Use kebab-case
- Descriptive but concise
- Match the feature name

### Step 5: Verify Documentation

Check your documentation:

✅ **Structure:**
- Starts with H2 (not H1)
- Logical flow
- All sections present

✅ **Content:**
- Clear and user-focused
- No technical jargon
- Accurate information
- Complete coverage

✅ **Screenshots:**
- Embedded at appropriate points
- Using CloudFront URLs
- Alt text provided
- Relevant to surrounding content

✅ **Formatting:**
- Valid markdown
- Consistent style
- No broken links
- Proper code blocks

### Step 6: Document Results

Provide a summary:

```markdown
## Documentation Created: [Feature Name]

**File:** `demo/docs/product_documentation/[category]/[feature-slug].md`
**Category:** [category]
**Word count:** ~[X] words
**Screenshots:** [X] embedded

### Structure:
- Overview
- Key Capabilities ([X] listed)
- How It Works ([X] workflows documented)
- Configuration ([X] options)
- Use Cases ([X] scenarios)
- FAQ ([X] questions)
- Support contact

### Screenshots Used:
1. [feature]-overview.png - [CloudFront URL]
2. [feature]-detail.png - [CloudFront URL]
[... list all ...]

### Next Steps:
1. Review documentation for accuracy
2. Sync to Pylon knowledge base using sync-docs skill
3. Include Pylon article URL in announcements
```

## Documentation Patterns by Category

### Features

Focus on:
- What the feature does
- How to use it
- Configuration options
- Common workflows

Length: 150-250 lines

### Integrations

Focus on:
- What service integrates with
- Setup process
- Authentication/authorization
- Available actions
- Troubleshooting

Length: 150-200 lines

### Getting Started

Focus on:
- Onboarding flow
- First-time setup
- Basic concepts
- Quick wins

Length: 100-150 lines

## Content Guidelines

### What to Include

✅ User benefits and value
✅ Step-by-step instructions
✅ Visual aids (screenshots)
✅ Configuration options
✅ Real-world examples
✅ Common questions

### What to Avoid

❌ Implementation details
❌ Code snippets (unless API docs)
❌ Internal terminology
❌ Assumptions about technical knowledge
❌ Marketing fluff
❌ Outdated information

## Troubleshooting

**Issue:** Can't find feature implementation in codebase

**Solution:**
- Search for related terms
- Check route definitions
- Look in frontend and backend
- Ask user for more context if genuinely unclear

**Issue:** Unclear what screenshots to use

**Solution:**
- Use overview screenshot in "Overview" section
- Use workflow screenshots in "How It Works"
- Use configuration screenshots in "Configuration"
- Place screenshots where they add context, not randomly

**Issue:** Feature too complex to document fully

**Solution:**
- Focus on main workflows (80% use cases)
- Link to advanced topics
- Keep it digestible
- Can create multiple docs for complex features

## Integration with Release Workflow

This skill is typically invoked as step 3 in the release workflow:

1. Capture screenshots (capture-screenshots skill)
2. Upload to Pylon CDN (sync-docs skill)
3. ✅ **Create documentation** ← You are here
4. Sync to Pylon (sync-docs skill)
5. Create announcements (create-changelog skill)

The CloudFront URLs from step 2 should be provided to this skill for embedding screenshots.
