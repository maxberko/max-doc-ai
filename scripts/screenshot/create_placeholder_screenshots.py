#!/usr/bin/env python3
"""Create placeholder screenshots for Release UI documentation"""
from PIL import Image, ImageDraw, ImageFont
import os

# Screenshot specifications
screenshots = [
    {
        'filename': 'release-ui-home.png',
        'title': 'max-doc-AI Home',
        'subtitle': 'Dashboard with Create New Release option',
        'description': 'Welcome screen\nwith navigation cards'
    },
    {
        'filename': 'release-ui-wizard-step1.png',
        'title': 'Release Wizard - Step 1',
        'subtitle': 'Feature Description',
        'description': 'Text area for\nfeature details'
    },
    {
        'filename': 'release-ui-wizard-step2.png',
        'title': 'Release Wizard - Step 2',
        'subtitle': 'Code Location',
        'description': 'Select: Current,\nLocal, or GitHub'
    },
    {
        'filename': 'release-ui-wizard-step3.png',
        'title': 'Release Wizard - Step 3',
        'subtitle': 'Release Date',
        'description': 'Date picker\nor "Today" option'
    },
    {
        'filename': 'release-ui-wizard-step4.png',
        'title': 'Release Wizard - Step 4',
        'subtitle': 'Review & Confirm',
        'description': 'Summary of\nall selections'
    },
    {
        'filename': 'release-ui-progress-active.png',
        'title': 'Release Execution',
        'subtitle': 'Live Progress Tracking',
        'description': 'Chat + Progress\nwith real-time updates'
    }
]

output_dir = '/Users/maxberko/code/max-doc-ai/demo/docs/product_documentation/screenshots'
os.makedirs(output_dir, exist_ok=True)

# Create each screenshot
for spec in screenshots:
    # Create image
    width, height = 1470, 840
    img = Image.new('RGB', (width, height), color='#dbe4ee')  # alice-blue
    draw = ImageDraw.Draw(img)

    # Draw header bar (steel-azure)
    draw.rectangle([0, 0, width, 80], fill='#054a91')

    # Draw main content area
    content_y = 120
    content_width = width - 160
    content_height = height - 200
    draw.rectangle([80, content_y, width-80, content_y + content_height], fill='#ffffff', outline='#3e7cb1', width=2)

    # Try to use a better font, fall back to default
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 48)
        subtitle_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
        desc_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()

    # Draw title on header
    draw.text((40, 25), 'max-doc-AI', fill='#ffffff', font=subtitle_font)

    # Draw content title
    draw.text((width//2, 220), spec['title'], fill='#054a91', font=title_font, anchor='mm')

    # Draw subtitle
    draw.text((width//2, 290), spec['subtitle'], fill='#3e7cb1', font=subtitle_font, anchor='mm')

    # Draw description
    draw.text((width//2, 450), spec['description'], fill='#054a91', font=desc_font, anchor='mm', align='center')

    # Draw accent element (harvest-orange)
    draw.ellipse([width//2-30, 550, width//2+30, 610], fill='#f17300')

    # Save
    output_path = os.path.join(output_dir, spec['filename'])
    img.save(output_path)
    print(f"✅ Created: {spec['filename']}")

print(f"\n📁 Screenshots saved to: {output_dir}")
print(f"📸 Total: {len(screenshots)} screenshots")
