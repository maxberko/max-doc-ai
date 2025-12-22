#!/usr/bin/env python3
"""
Migrate from old folder structure to new dated structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse


def migrate_to_dated_structure(
    old_base='./demo/docs/product_documentation',
    new_base='./output',
    release_date=None
):
    """
    Migrate existing docs to new dated structure

    Args:
        old_base: Old base directory
        new_base: New base directory
        release_date: Date to use (default: today)
    """
    if release_date is None:
        release_date = datetime.now().strftime('%Y-%m-%d')

    print(f"📦 Migrating documentation to dated structure")
    print(f"   From: {old_base}")
    print(f"   To: {new_base}")
    print(f"   Date: {release_date}")
    print()

    migrated_count = 0

    # Migrate features
    old_features = Path(old_base) / 'features'
    if old_features.exists():
        print("📄 Migrating features...")
        for feature_file in old_features.glob('*.md'):
            feature_slug = feature_file.stem
            new_dir = Path(new_base) / 'features' / f"{release_date}_{feature_slug}"
            new_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy2(feature_file, new_dir / feature_file.name)
            print(f"   ✅ Migrated feature: {feature_slug}")
            migrated_count += 1
        print()

    # Migrate changelogs
    old_changelog = Path(old_base) / 'changelog'
    if old_changelog.exists():
        print("📣 Migrating changelogs...")
        for feature_dir in old_changelog.iterdir():
            if feature_dir.is_dir():
                new_dir = Path(new_base) / 'changelogs' / release_date
                new_dir.mkdir(parents=True, exist_ok=True)

                # Copy all announcement files
                for file in feature_dir.glob('*'):
                    if file.is_file():
                        new_filename = f"{feature_dir.name}_{file.name}"
                        shutil.copy2(file, new_dir / new_filename)

                print(f"   ✅ Migrated changelog: {feature_dir.name}")
                migrated_count += 1
        print()

    # Migrate screenshots (optional - keep in screenshots folder)
    old_screenshots = Path(old_base) / 'screenshots'
    if old_screenshots.exists():
        print("📸 Copying screenshots...")
        new_screenshots_dir = Path(new_base) / 'screenshots'
        new_screenshots_dir.mkdir(parents=True, exist_ok=True)

        for screenshot in old_screenshots.glob('*.png'):
            shutil.copy2(screenshot, new_screenshots_dir / screenshot.name)
            print(f"   ✅ Copied: {screenshot.name}")
        print()

    print(f"✅ Migration complete! Migrated {migrated_count} items")
    print()
    print("Next steps:")
    print("1. Review the migrated files in the output/ directory")
    print("2. Update config.yaml to use new output structure")
    print("3. Set legacy_mode: false in config.yaml")
    print("4. Test the new structure with a release workflow")


def main():
    parser = argparse.ArgumentParser(
        description='Migrate documentation from old to new dated structure'
    )
    parser.add_argument(
        '--date',
        help='Release date (YYYY-MM-DD format, default: today)',
        default=None
    )
    parser.add_argument(
        '--old-base',
        help='Old base directory',
        default='./demo/docs/product_documentation'
    )
    parser.add_argument(
        '--new-base',
        help='New base directory',
        default='./output'
    )

    args = parser.parse_args()

    migrate_to_dated_structure(
        old_base=args.old_base,
        new_base=args.new_base,
        release_date=args.date
    )


if __name__ == '__main__':
    main()
