# Contributing to max-doc-AI

Thank you for considering contributing to max-doc-AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project follows a standard Code of Conduct:

- **Be respectful** - Treat everyone with respect and kindness
- **Be constructive** - Provide helpful feedback and suggestions
- **Be collaborative** - Work together to improve the project
- **Be inclusive** - Welcome contributors of all backgrounds and skill levels

## How Can I Contribute?

### Types of Contributions

We welcome contributions in many forms:

- **Bug fixes** - Identify and fix bugs in the code
- **New features** - Add new capabilities or integrations
- **Documentation** - Improve setup guides, usage examples, or API docs
- **Examples** - Create new demo workflows or use cases
- **Testing** - Add test coverage or improve testing infrastructure
- **Code quality** - Refactoring, optimization, or modernization

### Good First Issues

Look for issues tagged with:
- `good first issue` - Great for newcomers
- `help wanted` - Community assistance requested
- `documentation` - Documentation improvements needed

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Claude Code CLI installed
- Git for version control
- Pylon account (for testing integrations)

### Installation

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/max-doc-ai.git
   cd max-doc-ai
   ```

2. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure for testing**
   ```bash
   # Copy example configs
   cp config.example.yaml config.yaml
   cp .env.example .env

   # Edit with your test credentials
   # Use a separate test Pylon KB, not production!
   ```

5. **Verify installation**
   ```bash
   python3 scripts/config.py
   ```

### Development Environment

**Recommended Tools:**
- **VS Code** or **PyCharm** for Python development
- **Python virtual environment** to isolate dependencies
- **Git** with commit signing enabled

**Virtual Environment Setup:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
max-doc-ai/
├── .claude/
│   └── skills/              # Claude Code skills (main functionality)
│       ├── create-release/  # Orchestrator skill
│       ├── capture-screenshots/
│       ├── update-product-doc/
│       ├── sync-docs/
│       └── create-changelog/
├── scripts/
│   ├── config.py            # Configuration loader
│   ├── auth_manager.py      # Authentication setup
│   ├── pylon/               # Pylon API integration
│   │   ├── upload.py        # Screenshot upload
│   │   ├── sync.py          # Documentation sync
│   │   └── converter.py     # Markdown to HTML
│   ├── screenshot/          # Screenshot capture
│   │   └── capture.py       # Computer Use automation
│   └── utils/               # Utilities
│       └── state.py         # State tracking
├── demo/                    # Example documentation
├── docs/                    # Setup and usage guides
├── config.example.yaml      # Configuration template
├── .env.example             # Environment template
└── requirements.txt         # Python dependencies
```

### Key Components

**Claude Skills** (`.claude/skills/`)
- Written in markdown with embedded instructions
- Called via `@claude Skill: skill-name`
- See [Claude Code Skills Documentation](https://docs.anthropic.com/claude-code/skills)

**Python Scripts** (`scripts/`)
- Core automation logic
- Pylon API integration
- Screenshot capture
- State management

**Configuration** (`config.yaml`, `.env`)
- Product settings
- Pylon credentials
- Workflow options

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def upload_screenshot(image_path: str, alt_text: str = '') -> Optional[Dict]:
    """Upload a screenshot to Pylon CDN.

    Args:
        image_path: Path to the image file
        alt_text: Alternative text for accessibility

    Returns:
        Dict with upload result or None if failed
    """
    if not os.path.exists(image_path):
        return None

    # Implementation...
```

**Key Points:**
- Use type hints for function parameters and returns
- Write docstrings for all functions and classes
- Use meaningful variable names
- Keep functions focused and single-purpose
- Add comments for complex logic

### File Naming

- Python files: `lowercase_with_underscores.py`
- Markdown files: `lowercase-with-hyphens.md`
- Configuration: `config.yaml`, `.env`

### Import Organization

```python
# Standard library imports
import os
import json
from pathlib import Path

# Third-party imports
import requests
from anthropic import Anthropic

# Local imports
import config as cfg
from utils import state
```

### Error Handling

```python
# Good - Specific exceptions with helpful messages
try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
    return None
except requests.exceptions.ConnectionError:
    print(f"❌ Connection failed - check your network")
    return None
```

### Logging and Output

Use clear, user-friendly messages:

```python
print(f"📸 Capturing screenshot: {url}")
print(f"   ✅ Saved: {filename}")
print(f"   ⚠️  Warning: {warning_message}")
print(f"   ❌ Error: {error_message}")
```

## Testing

### Manual Testing

Before submitting a PR:

1. **Test individual components**
   ```bash
   # Test configuration
   python3 scripts/config.py

   # Test authentication
   python3 scripts/auth_manager.py

   # Test Pylon upload
   python3 scripts/pylon/upload.py

   # Test state management
   python3 scripts/utils/state.py --summary
   ```

2. **Test skills**
   ```bash
   # Test each skill individually
   @claude Skill: capture-screenshots
   @claude Skill: update-product-doc
   @claude Skill: sync-docs
   @claude Skill: create-changelog

   # Test complete workflow
   @claude Skill: create-release
   ```

3. **Verify outputs**
   - Check generated files for correctness
   - Verify Pylon articles are created properly
   - Test that links work and images load
   - Review state file for accuracy

### Test Environment

**Important:** Always use a separate test environment:
- Separate Pylon Knowledge Base for testing
- Test collections (not production)
- Sample product URLs (or staging environment)
- Test authentication credentials

**Never test with:**
- Production Pylon KB
- Customer-facing collections
- Live product data
- Production credentials

## Pull Request Process

### Before Submitting

1. **Test your changes thoroughly**
   - Run manual tests (see [Testing](#testing))
   - Verify no regressions in existing functionality
   - Test edge cases and error conditions

2. **Update documentation**
   - Add/update docstrings for new functions
   - Update relevant markdown docs
   - Add examples if introducing new features
   - Update README if needed

3. **Clean up your commits**
   ```bash
   # Make atomic commits with clear messages
   git add specific-file.py
   git commit -m "Add retry logic to Pylon upload"

   # Squash if needed
   git rebase -i HEAD~3
   ```

4. **Ensure no secrets are committed**
   ```bash
   # Check for sensitive data
   git diff --cached | grep -i "api_key\|password\|secret"

   # Make sure .env and config.yaml are in .gitignore
   ```

### Creating the Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a PR on GitHub**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

3. **PR Title Format**
   ```
   Add: [New feature description]
   Fix: [Bug fix description]
   Docs: [Documentation change]
   Refactor: [Code improvement]
   Test: [Testing improvement]
   ```

4. **PR Description Template**
   ```markdown
   ## Description
   [Clear description of what this PR does]

   ## Motivation
   [Why is this change needed?]

   ## Changes
   - [Change 1]
   - [Change 2]
   - [Change 3]

   ## Testing
   [How did you test this?]

   ## Screenshots (if applicable)
   [Add screenshots for UI changes]

   ## Checklist
   - [ ] Tested manually
   - [ ] Documentation updated
   - [ ] No secrets committed
   - [ ] Follows coding standards
   ```

### Review Process

1. **Automated checks** (if configured)
   - Linting passes
   - No security issues detected

2. **Maintainer review**
   - Code quality assessment
   - Architecture alignment
   - Documentation completeness

3. **Feedback and iteration**
   - Address review comments
   - Push additional commits
   - Re-request review

4. **Approval and merge**
   - Maintainer approves
   - PR is merged
   - Branch is deleted

## Reporting Bugs

### Before Reporting

1. **Check existing issues** - Search to see if already reported
2. **Try latest version** - Update and test if bug still exists
3. **Reproduce the issue** - Ensure it's consistent

### Bug Report Template

```markdown
## Description
[Clear description of the bug]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [And so on...]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.2]
- Claude Code version: [e.g., 1.2.3]
- Anthropic SDK version: [e.g., 0.40.0]

## Screenshots or Logs
[If applicable, add screenshots or error logs]

## Additional Context
[Any other relevant information]
```

## Suggesting Enhancements

### Enhancement Request Template

```markdown
## Feature Description
[Clear description of the proposed feature]

## Use Case
[Why is this feature needed? What problem does it solve?]

## Proposed Solution
[How would you implement this?]

## Alternatives Considered
[What other approaches did you consider?]

## Additional Context
[Any other relevant information, mockups, examples]
```

### Enhancement Areas

We're particularly interested in:

- **New CDN Providers** - Support for Cloudinary, S3, etc.
- **Additional Channels** - Discord, Teams, in-app notifications
- **Video Support** - Automated demo recording
- **Multi-language** - Documentation in multiple languages
- **Versioning** - Per-release documentation management
- **Other Knowledge Bases** - Notion, GitBook, Confluence integrations
- **CI/CD Integration** - GitHub Actions, GitLab CI workflows

## Communication

### Where to Ask Questions

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Requests** - Code-specific questions

### Response Times

- **Bug reports** - Usually reviewed within 1-2 days
- **Feature requests** - Reviewed weekly
- **Pull requests** - Initial review within 3-5 days

## Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0, the same license as the project. See the [LICENSE](LICENSE) file for details.

**Important for contributors:**
- All contributions become GPL v3
- Derivative works must also be GPL v3
- You retain copyright but grant GPL v3 rights
- Commercial use is allowed but source must be provided

## Questions?

If you have questions about contributing:
- Open a GitHub Discussion
- Check existing documentation
- Review closed PRs for examples

---

**Thank you for contributing to max-doc-AI!** Every contribution, no matter how small, helps improve the project for everyone.
