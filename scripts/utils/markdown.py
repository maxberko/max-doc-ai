"""
Markdown utilities for max-doc-AI

Helper functions for parsing and manipulating markdown documentation.
"""

import re
from typing import Dict, Optional, Tuple


def extract_title(md_content: str) -> Optional[str]:
    """
    Extract the H1 title from markdown content

    Args:
        md_content: Markdown content string

    Returns:
        Title string, or None if no H1 found
    """
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return None


def extract_frontmatter(md_content: str) -> Tuple[Optional[Dict], str]:
    """
    Extract YAML frontmatter from markdown content

    Frontmatter format:
    ---
    key: value
    another_key: another_value
    ---
    # Content starts here

    Args:
        md_content: Markdown content string

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    if not md_content.startswith('---'):
        return None, md_content

    # Find the closing ---
    parts = md_content[3:].split('---', 1)
    if len(parts) != 2:
        return None, md_content

    frontmatter_text, content = parts

    # Parse frontmatter (simple key: value format)
    frontmatter = {}
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, content.lstrip()


def add_frontmatter(md_content: str, frontmatter: Dict) -> str:
    """
    Add or update YAML frontmatter in markdown content

    Args:
        md_content: Markdown content string
        frontmatter: Dict of frontmatter key-value pairs

    Returns:
        Markdown content with frontmatter
    """
    # Remove existing frontmatter if present
    _, content = extract_frontmatter(md_content)

    # Build frontmatter
    fm_lines = ['---']
    for key, value in frontmatter.items():
        fm_lines.append(f'{key}: {value}')
    fm_lines.append('---')
    fm_lines.append('')

    return '\n'.join(fm_lines) + content


def extract_image_references(md_content: str) -> list:
    """
    Extract all image references from markdown

    Finds both markdown format ![alt](url) and HTML <img> tags

    Args:
        md_content: Markdown content string

    Returns:
        List of dicts with 'alt' and 'url' keys
    """
    images = []

    # Find markdown images: ![alt text](url)
    md_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    for match in re.finditer(md_pattern, md_content):
        alt = match.group(1)
        url = match.group(2)
        images.append({'alt': alt, 'url': url, 'format': 'markdown'})

    # Find HTML images: <img src="url" alt="alt text">
    html_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>'
    for match in re.finditer(html_pattern, md_content):
        url = match.group(1)
        alt = match.group(2)
        images.append({'alt': alt, 'url': url, 'format': 'html'})

    return images


def replace_image_urls(md_content: str, url_mapping: Dict[str, str]) -> str:
    """
    Replace image URLs in markdown content

    Args:
        md_content: Markdown content string
        url_mapping: Dict mapping old URLs to new URLs

    Returns:
        Markdown content with updated URLs
    """
    result = md_content

    for old_url, new_url in url_mapping.items():
        # Replace in markdown format
        result = result.replace(f']({old_url})', f']({new_url})')

        # Replace in HTML format
        result = result.replace(f'src="{old_url}"', f'src="{new_url}"')

    return result


def count_words(md_content: str) -> int:
    """
    Count words in markdown content (excluding code blocks)

    Args:
        md_content: Markdown content string

    Returns:
        Word count
    """
    # Remove code blocks
    content = re.sub(r'```.*?```', '', md_content, flags=re.DOTALL)

    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)

    # Remove markdown syntax
    content = re.sub(r'[#*_\[\]()]', '', content)

    # Count words
    words = content.split()
    return len(words)


def extract_headings(md_content: str) -> list:
    """
    Extract all headings from markdown content

    Args:
        md_content: Markdown content string

    Returns:
        List of dicts with 'level' (1-6) and 'text' keys
    """
    headings = []

    for line in md_content.split('\n'):
        if line.startswith('#'):
            # Count # characters for heading level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break

            if 1 <= level <= 6:
                text = line[level:].strip()
                headings.append({'level': level, 'text': text})

    return headings


def validate_markdown_structure(md_content: str) -> Tuple[bool, list]:
    """
    Validate markdown structure

    Checks for:
    - Presence of H1 heading
    - Proper heading hierarchy (no skipping levels)
    - Valid image references

    Args:
        md_content: Markdown content string

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    headings = extract_headings(md_content)

    # Check for H1
    h1_count = sum(1 for h in headings if h['level'] == 1)
    if h1_count == 0:
        issues.append("No H1 heading found")
    elif h1_count > 1:
        issues.append(f"Multiple H1 headings found ({h1_count})")

    # Check heading hierarchy
    prev_level = 0
    for heading in headings:
        level = heading['level']
        if level > prev_level + 1:
            issues.append(f"Heading hierarchy skip: H{prev_level} to H{level}")
        prev_level = level

    # Check for broken image references
    images = extract_image_references(md_content)
    for img in images:
        if not img['url'].strip():
            issues.append(f"Empty image URL for: {img['alt']}")

    is_valid = len(issues) == 0
    return is_valid, issues


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 markdown.py <file.md>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r') as f:
        content = f.read()

    # Analyze markdown
    print("Markdown Analysis")
    print("=" * 60)

    title = extract_title(content)
    print(f"Title: {title}")

    words = count_words(content)
    print(f"Word count: {words}")

    headings = extract_headings(content)
    print(f"\nHeadings ({len(headings)}):")
    for h in headings:
        indent = "  " * (h['level'] - 1)
        print(f"{indent}H{h['level']}: {h['text']}")

    images = extract_image_references(content)
    print(f"\nImages ({len(images)}):")
    for img in images:
        print(f"  • {img['alt']}: {img['url']}")

    is_valid, issues = validate_markdown_structure(content)
    print(f"\nValidation: {'✅ Valid' if is_valid else '❌ Issues found'}")
    if issues:
        for issue in issues:
            print(f"  • {issue}")
