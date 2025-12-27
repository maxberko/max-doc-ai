#!/usr/bin/env python3
"""
Generic Image Upload Script

Uploads images to any KB provider's CDN/storage (Pylon, Zendesk, etc.)
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List

# Add project root to path (must be first for utils/ imports)
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from utils.kb_providers import get_provider


def upload_image(
    provider_name: str,
    image_path: str,
    alt_text: str = "",
    caption: str = "",
    provider_config: dict = None
) -> dict:
    """
    Upload a single image to KB provider

    Args:
        provider_name: Name of KB provider ('pylon', 'zendesk', etc.)
        image_path: Path to the image file
        alt_text: Alternative text for accessibility
        caption: Image caption
        provider_config: Optional provider config (defaults to config.yaml)

    Returns:
        Dict with image URL and metadata, or None if failed
    """
    # Get provider configuration
    if provider_config is None:
        provider_config = get_provider_config(provider_name)

    # Initialize provider
    provider = get_provider(provider_name, provider_config)
    if not provider:
        return None

    # Upload image
    result = provider.upload_image(image_path, alt_text, caption)

    if result:
        return {
            'url': result.url,
            'filename': result.filename,
            'alt_text': result.alt_text,
            'caption': result.caption,
            'provider_id': result.provider_id,
            'provider': provider_name
        }
    else:
        return None


def upload_images_batch(
    provider_name: str,
    images: List[Dict],
    provider_config: dict = None
) -> Dict[str, Dict]:
    """
    Upload multiple images

    Args:
        provider_name: KB provider name
        images: List of dicts with 'name', 'path', 'alt', 'caption'
        provider_config: Optional provider config

    Returns:
        Dict mapping image names to upload results
    """
    print(f"\n📤 Uploading {len(images)} images to {provider_name.upper()}...\n")

    # Get provider configuration
    if provider_config is None:
        provider_config = get_provider_config(provider_name)

    # Initialize provider
    provider = get_provider(provider_name, provider_config)
    if not provider:
        return {}

    # Upload batch
    results = provider.upload_images_batch(images)

    # Convert ImageUpload objects to dicts
    results_dict = {}
    for name, upload in results.items():
        results_dict[name] = {
            'url': upload.url,
            'filename': upload.filename,
            'alt_text': upload.alt_text,
            'caption': upload.caption,
            'provider_id': upload.provider_id,
            'provider': provider_name
        }

    return results_dict


def upload_from_metadata_file(provider_name: str, metadata_file: str) -> Dict[str, Dict]:
    """
    Read screenshot metadata and upload to KB provider

    Args:
        provider_name: KB provider name
        metadata_file: Path to JSON file with screenshot metadata

    Returns:
        Dict mapping screenshot names to CDN URLs
    """
    if not os.path.exists(metadata_file):
        print(f"❌ Metadata file not found: {metadata_file}")
        return {}

    with open(metadata_file, 'r') as f:
        images = json.load(f)

    results = upload_images_batch(provider_name, images)

    # Save upload results
    results_file = metadata_file.replace('.json', f'-uploaded-{provider_name}.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"📝 Upload results saved: {results_file}")

    return results


def get_provider_config(provider_name: str = None) -> dict:
    """
    Get provider configuration from config.yaml

    Args:
        provider_name: Provider name ('pylon', 'zendesk', etc.) or None for default

    Returns:
        Provider configuration dict
    """
    try:
        kb_info = cfg.get_kb_config()

        # Use specified provider or default from config
        if not provider_name:
            provider_name = kb_info['provider']

        # If requesting specific provider, get its config
        if provider_name != kb_info['provider']:
            config = cfg.get_config()
            kb_config = config.get('knowledge_base', {})
            providers = kb_config.get('providers', {})
            provider_config = providers.get(provider_name)

            if not provider_config:
                raise ValueError(
                    f"Provider '{provider_name}' not found in config.yaml.\n"
                    f"Available providers: {list(providers.keys())}"
                )
            return provider_config

        return kb_info['config']

    except Exception as e:
        # Try old Pylon-only format for backwards compatibility
        if provider_name in [None, 'pylon']:
            return cfg.get_pylon_config()
        raise e


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Upload images to KB provider CDN'
    )
    parser.add_argument(
        '--provider',
        help='KB provider name (pylon, zendesk, etc.)',
        default=None
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

    # Determine provider
    if not args.provider:
        config = cfg.get_config()
        provider_name = config.get('knowledge_base', {}).get('provider', 'pylon')
    else:
        provider_name = args.provider

    print(f"📤 Image Upload Tool ({provider_name.upper()})")
    print("=" * 60)

    if args.image:
        # Upload single image
        result = upload_image(provider_name, args.image, alt_text=args.alt)
        if result:
            print(f"\n✅ Image URL: {result['url']}")
        else:
            print("\n❌ Upload failed")
            sys.exit(1)
    elif args.metadata_file:
        # Upload from metadata file
        upload_from_metadata_file(provider_name, args.metadata_file)
    else:
        print("\n⚠️  Please provide either --image or a metadata file")
        print("   Usage:")
        print(f"     python3 upload.py metadata.json [--provider {provider_name}]")
        print(f"     python3 upload.py --image screenshot.png --alt 'Dashboard view' [--provider {provider_name}]")
