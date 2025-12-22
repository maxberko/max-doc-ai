#!/usr/bin/env python3
"""
Markdown to HTML converter with Pylon-specific React wrappers

This module converts markdown documentation to HTML with special React component
wrappers required by Pylon's knowledge base system.

IMPORTANT: Pylon requires images to be wrapped in a specific React component structure.
This is NOT optional - images without this structure will not render correctly.
"""

import re
import markdown


def remove_h1_heading(md_content):
    """
    Remove H1 heading from markdown

    Pylon displays the article title separately, so we remove the H1 from the body
    to avoid duplication.

    Args:
        md_content: Markdown content string

    Returns:
        Markdown content without H1 heading
    """
    lines = md_content.split('\n')
    if lines and lines[0].startswith('# '):
        # Skip first line (H1) and the empty line after it if present
        if len(lines) > 1 and lines[1].strip() == '':
            return '\n'.join(lines[2:])
        return '\n'.join(lines[1:])
    return md_content


def convert_images_to_react_wrappers(html_content):
    """
    Convert simple img tags to full React node-imageBlock wrappers

    CRITICAL: Pylon requires this exact React component structure for images.
    Do not modify this structure unless Pylon's requirements change.

    Args:
        html_content: HTML content with <img> tags

    Returns:
        HTML content with images wrapped in React components
    """
    def wrap_img(match):
        img_tag = match.group(0)

        # Extract src and alt from img tag
        src_match = re.search(r'src="([^"]*)"', img_tag)
        alt_match = re.search(r'alt="([^"]*)"', img_tag)

        src = src_match.group(1) if src_match else ""
        alt = alt_match.group(1) if alt_match else ""

        # Build full React wrapper (REQUIRED by Pylon)
        # This exact structure is needed for images to render correctly
        react_wrapper = f'''<div class="react-renderer node-imageBlock" contenteditable="false" draggable="true">
  <div data-node-view-wrapper="" style="white-space: normal;">
    <button aria-label="Preview image: Preview" class="inline-block w-full cursor-zoom-in">
      <div class="ml-auto mr-auto mx-auto" style="width: 100%;">
        <div contenteditable="false">
          <img class="block" alt="{alt}" data-drag-handle="false" src="{src}">
        </div>
      </div>
    </button>
    <dialog class="dialog" data-is-modal="true" style="--backdrop-visibility: 1;"></dialog>
  </div>
</div>'''

        return react_wrapper

    # Replace all img tags with React wrappers
    html_with_wrappers = re.sub(r'<img[^>]*>', wrap_img, html_content)

    return html_with_wrappers


def ensure_unencoded_ampersands(html_content):
    """
    Ensure ampersands in URLs are unencoded

    Pylon requires unencoded & characters in URLs (not &amp;).
    CloudFront URLs often contain query parameters with &.

    Args:
        html_content: HTML content

    Returns:
        HTML content with unencoded ampersands in src attributes
    """
    # Replace &amp; with & in src attributes only
    def fix_src_ampersands(match):
        src_value = match.group(1)
        # Replace &amp; with & in the src value
        fixed_value = src_value.replace('&amp;', '&')
        return f'src="{fixed_value}"'

    html_fixed = re.sub(r'src="([^"]*)"', fix_src_ampersands, html_content)
    return html_fixed


def markdown_to_html_with_react_images(md_content, remove_h1=True):
    """
    Convert markdown to HTML and wrap images in React structures

    This is the main conversion function that handles the full pipeline:
    1. Remove H1 heading (optional)
    2. Convert markdown to HTML
    3. Wrap images in React components
    4. Ensure proper URL encoding

    Args:
        md_content: Markdown content string
        remove_h1: Whether to remove H1 heading (default: True)

    Returns:
        HTML content ready for Pylon
    """
    # Step 1: Remove H1 heading if requested
    if remove_h1:
        md_content = remove_h1_heading(md_content)

    # Step 2: Convert markdown to HTML
    html = markdown.markdown(
        md_content,
        extensions=['extra', 'nl2br', 'fenced_code', 'tables']
    )

    # Step 3: Wrap all images in React node-imageBlock structure
    html_with_react = convert_images_to_react_wrappers(html)

    # Step 4: Ensure unencoded ampersands in URLs
    html_final = ensure_unencoded_ampersands(html_with_react)

    return html_final


def validate_react_wrappers(html_content):
    """
    Validate that all images are properly wrapped in React components

    Args:
        html_content: HTML content to validate

    Returns:
        tuple: (is_valid, image_count, error_message)
    """
    # Count React-wrapped images
    react_images = html_content.count('node-imageBlock')

    # Count plain img tags (should be 0 if all are wrapped)
    # Look for img tags NOT inside node-imageBlock wrappers
    plain_img_pattern = r'<img[^>]*>'
    all_imgs = len(re.findall(plain_img_pattern, html_content))

    if react_images != all_imgs:
        return False, react_images, f"Found {all_imgs} img tags but only {react_images} React wrappers"

    if react_images == 0 and all_imgs == 0:
        return True, 0, "No images found"

    return True, react_images, f"All {react_images} images properly wrapped"


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert markdown to Pylon-compatible HTML'
    )
    parser.add_argument(
        'input_file',
        help='Input markdown file'
    )
    parser.add_argument(
        '--output',
        help='Output HTML file (default: print to stdout)'
    )
    parser.add_argument(
        '--keep-h1',
        action='store_true',
        help='Keep H1 heading (default: remove it)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate React wrappers'
    )

    args = parser.parse_args()

    # Read markdown file
    with open(args.input_file, 'r') as f:
        md_content = f.read()

    # Convert
    html_content = markdown_to_html_with_react_images(
        md_content,
        remove_h1=not args.keep_h1
    )

    # Validate if requested
    if args.validate:
        is_valid, count, message = validate_react_wrappers(html_content)
        print(f"\n{'✅' if is_valid else '❌'} {message}", file=sys.stderr)

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(html_content)
        print(f"✅ HTML written to: {args.output}", file=sys.stderr)
    else:
        print(html_content)
