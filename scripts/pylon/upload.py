#!/usr/bin/env python3
"""
Upload screenshots to Pylon's Attachments API

This module handles uploading images to Pylon and returns CloudFront URLs
for use in articles.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
import config as cfg


class PylonUploader:
    """Handles uploading images to Pylon's Attachments API"""

    def __init__(self, api_key=None, kb_id=None):
        """
        Initialize Pylon uploader

        Args:
            api_key: Pylon API key (default: from config)
            kb_id: Pylon Knowledge Base ID (default: from config)
        """
        config = cfg.get_pylon_config()

        self.api_key = api_key or config['api_key']
        self.kb_id = kb_id or config['kb_id']
        self.base_url = config['api_base']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def upload_image(self, image_path: str, alt_text: str = '', caption: str = '') -> Optional[Dict]:
        """
        Upload an image to Pylon's Attachments API

        Args:
            image_path: Path to the image file
            alt_text: Alternative text for accessibility
            caption: Caption for the image

        Returns:
            Dict with image URL and metadata, or None if failed
        """
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None

        print(f"📤 Uploading: {Path(image_path).name}...")

        # Prepare the file for upload
        filename = Path(image_path).name
        with open(image_path, 'rb') as f:
            files = {
                'file': (filename, f, f'image/{Path(image_path).suffix[1:]}')
            }

            # Add metadata if provided
            data = {}
            if alt_text:
                data['alt_text'] = alt_text
            if caption:
                data['caption'] = caption

            # Make the upload request
            url = f'{self.base_url}/attachments'

            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    files=files,
                    data=data
                )

                if response.status_code in [200, 201]:
                    result = response.json()
                    image_url = result.get('data', {}).get('url')

                    if image_url:
                        print(f"   ✅ Uploaded: {image_url}")
                        return {
                            'url': image_url,
                            'filename': filename,
                            'alt_text': alt_text,
                            'caption': caption,
                            'pylon_id': result.get('data', {}).get('id')
                        }
                    else:
                        print(f"   ⚠️  No URL in response: {result}")
                        return None
                else:
                    print(f"   ❌ Upload failed: {response.status_code}")
                    print(f"      Response: {response.text}")
                    return None

            except Exception as e:
                print(f"   ❌ Error uploading: {e}")
                return None

    def upload_batch(self, screenshots: List[Dict]) -> Dict[str, Dict]:
        """
        Upload multiple screenshots

        Args:
            screenshots: List of screenshot metadata dicts with 'path', 'name', 'alt', 'caption'

        Returns:
            Dict mapping screenshot names to upload results
        """
        results = {}

        print(f"\n📤 Uploading {len(screenshots)} screenshots to Pylon...\n")

        for screenshot in screenshots:
            name = screenshot.get('name')
            path = screenshot.get('path')
            alt_text = screenshot.get('alt', '')
            caption = screenshot.get('caption', '')

            result = self.upload_image(path, alt_text, caption)

            if result:
                results[name] = result
            else:
                print(f"   ⚠️  Skipping {name} due to upload failure")

        print(f"\n✅ Successfully uploaded {len(results)}/{len(screenshots)} images")

        return results


def upload_screenshots_from_metadata(metadata_file: str) -> Dict[str, Dict]:
    """
    Read screenshot metadata and upload to Pylon

    Args:
        metadata_file: Path to JSON file with screenshot metadata

    Returns:
        Dict mapping screenshot names to Pylon URLs
    """
    if not os.path.exists(metadata_file):
        print(f"❌ Metadata file not found: {metadata_file}")
        return {}

    with open(metadata_file, 'r') as f:
        screenshots = json.load(f)

    uploader = PylonUploader()
    results = uploader.upload_batch(screenshots)

    # Save upload results
    results_file = metadata_file.replace('.json', '-uploaded.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"📝 Upload results saved: {results_file}")

    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Upload screenshots to Pylon CDN'
    )
    parser.add_argument(
        'metadata_file',
        nargs='?',
        help='JSON file with screenshot metadata'
    )
    parser.add_argument(
        '--image',
        help='Upload a single image file'
    )
    parser.add_argument(
        '--alt',
        help='Alt text for single image',
        default=''
    )

    args = parser.parse_args()

    print("📤 Pylon Image Upload Tool")
    print("=" * 60)

    if args.image:
        # Upload single image
        uploader = PylonUploader()
        result = uploader.upload_image(args.image, alt_text=args.alt)
        if result:
            print(f"\n✅ Image URL: {result['url']}")
    elif args.metadata_file:
        # Upload from metadata file
        upload_screenshots_from_metadata(args.metadata_file)
    else:
        print("\n⚠️  Please provide either --image or a metadata file")
        print("   Usage:")
        print("     python3 upload.py metadata.json")
        print("     python3 upload.py --image screenshot.png --alt 'Dashboard view'")
