#!/usr/bin/env python3
"""
Documentation Inventory Manager

Scans and catalogs existing documentation to understand:
- What docs exist and where
- What's been synced vs what needs syncing
- Documentation structure and organization
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import re

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / 'scripts') not in sys.path:
    sys.path.append(str(PROJECT_ROOT / 'scripts'))

import config as cfg
from scripts.utils import state as state_manager  # From scripts/utils, not project/utils


@dataclass
class DocumentInfo:
    """Information about a documentation file"""
    path: str
    filename: str
    category: str
    title: Optional[str] = None
    slug: Optional[str] = None
    feature_date: Optional[str] = None  # For dated features (YYYY-MM-DD)
    size_bytes: int = 0
    modified_at: Optional[str] = None
    synced: bool = False
    sync_provider: Optional[str] = None
    sync_date: Optional[str] = None
    public_url: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class DocumentInventory:
    """Scan and catalog documentation"""

    def __init__(self, base_paths: List[str] = None):
        """
        Initialize inventory scanner

        Args:
            base_paths: List of paths to scan (defaults to config paths)
        """
        if base_paths is None:
            base_paths = self._get_default_paths()

        self.base_paths = base_paths
        self.documents: List[DocumentInfo] = []

    def _get_default_paths(self) -> List[str]:
        """Get default documentation paths from config"""
        paths = []

        try:
            # Try documentation base path
            doc_config = cfg.get_documentation_config()
            if 'base_path' in doc_config:
                paths.append(doc_config['base_path'])
        except:
            pass

        try:
            # Try output directory
            output_config = cfg.get_output_config()
            output_base = output_config.get('base_dir', './output')
            if not os.path.isabs(output_base):
                project_root = Path(__file__).parent.parent
                output_base = str(project_root / output_base)
            paths.append(output_base)
        except:
            pass

        # Fallback defaults
        if not paths:
            project_root = Path(__file__).parent.parent
            paths = [
                str(project_root / 'demo/docs/product_documentation'),
                str(project_root / 'output')
            ]

        return [p for p in paths if os.path.exists(p)]

    def scan(self) -> List[DocumentInfo]:
        """
        Scan all configured paths for documentation

        Returns:
            List of DocumentInfo objects
        """
        self.documents = []

        print(f"🔍 Scanning documentation in {len(self.base_paths)} location(s)...")

        for base_path in self.base_paths:
            print(f"\n📂 Scanning: {base_path}")
            self._scan_directory(base_path)

        # Load sync state and mark synced docs
        self._load_sync_state()

        print(f"\n✅ Found {len(self.documents)} documentation file(s)")

        return self.documents

    def _scan_directory(self, base_path: str):
        """Recursively scan a directory for markdown files"""
        for root, dirs, files in os.walk(base_path):
            # Skip hidden directories and common excludes
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    full_path = os.path.join(root, file)
                    doc_info = self._parse_document(full_path, base_path)
                    if doc_info:
                        self.documents.append(doc_info)

    def _parse_document(self, file_path: str, base_path: str) -> Optional[DocumentInfo]:
        """Parse a markdown file and extract metadata"""
        try:
            # Get file stats
            stat = os.stat(file_path)
            modified_at = datetime.fromtimestamp(stat.st_mtime).isoformat()

            # Determine category from path
            rel_path = os.path.relpath(file_path, base_path)
            parts = Path(rel_path).parts

            category = 'unknown'
            feature_date = None
            slug = None

            # Try to infer category from path structure
            if 'features' in parts:
                category = 'features'
                # Check for dated feature folders (YYYY-MM-DD_slug)
                for part in parts:
                    match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)', part)
                    if match:
                        feature_date = match.group(1)
                        slug = match.group(2)
                        break
            elif 'getting-started' in parts:
                category = 'getting-started'
            elif 'integrations' in parts:
                category = 'integrations'
            elif 'changelog' in parts or 'changelogs' in parts:
                category = 'changelog'

            # Extract title from markdown (first H1)
            title = self._extract_title(file_path)

            # Derive slug from filename if not already set
            if not slug:
                slug = Path(file_path).stem

            return DocumentInfo(
                path=file_path,
                filename=Path(file_path).name,
                category=category,
                title=title,
                slug=slug,
                feature_date=feature_date,
                size_bytes=stat.st_size,
                modified_at=modified_at
            )

        except Exception as e:
            print(f"   ⚠️  Error parsing {file_path}: {e}")
            return None

    def _extract_title(self, file_path: str) -> Optional[str]:
        """Extract title from markdown file (first H1)"""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('# '):
                        return line[2:].strip()
                    # Stop after first 20 lines
                    if f.tell() > 1000:
                        break
        except:
            pass
        return None

    def _load_sync_state(self):
        """Load sync state and mark which docs have been synced"""
        try:
            state_data = state_manager.load_state()
            articles = state_data.get('articles', {})

            for doc in self.documents:
                # Try to find matching article in state
                # State keys are typically: provider:category-slug
                possible_keys = [
                    f"{doc.category}-{doc.slug}",
                    doc.slug,
                ]

                for state_key, article_data in articles.items():
                    # Check if this state entry matches the doc
                    for key in possible_keys:
                        if key in state_key:
                            doc.synced = True
                            doc.sync_provider = article_data.get('provider', 'unknown')
                            doc.sync_date = article_data.get('synced_at')
                            doc.public_url = article_data.get('public_url')
                            break

        except Exception as e:
            print(f"   ⚠️  Could not load sync state: {e}")

    def filter_by_category(self, category: str) -> List[DocumentInfo]:
        """Filter documents by category"""
        return [doc for doc in self.documents if doc.category == category]

    def filter_synced(self, synced: bool = True) -> List[DocumentInfo]:
        """Filter documents by sync status"""
        return [doc for doc in self.documents if doc.synced == synced]

    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        return sorted(set(doc.category for doc in self.documents))

    def print_summary(self):
        """Print a formatted summary of the inventory"""
        print("\n" + "=" * 70)
        print("📊 Documentation Inventory Summary")
        print("=" * 70)

        # By category
        categories = self.get_categories()
        print(f"\n📚 By Category:")
        for category in categories:
            docs = self.filter_by_category(category)
            synced_count = sum(1 for d in docs if d.synced)
            print(f"  {category}: {len(docs)} total, {synced_count} synced")

        # By sync status
        synced = self.filter_synced(True)
        unsynced = self.filter_synced(False)

        print(f"\n🔄 Sync Status:")
        print(f"  ✅ Synced: {len(synced)}")
        print(f"  ⏳ Not Synced: {len(unsynced)}")

        # Recent documents
        recent = sorted(self.documents, key=lambda d: d.modified_at or '', reverse=True)[:5]
        if recent:
            print(f"\n📝 Recent Documents:")
            for doc in recent:
                status = "✅" if doc.synced else "⏳"
                print(f"  {status} {doc.title or doc.filename} ({doc.category})")

        print("\n" + "=" * 70 + "\n")

    def print_details(self, show_synced: bool = True, show_unsynced: bool = True):
        """Print detailed list of all documents"""
        print("\n" + "=" * 70)
        print("📄 Documentation Details")
        print("=" * 70)

        categories = self.get_categories()

        for category in categories:
            docs = self.filter_by_category(category)

            print(f"\n📁 {category.upper()} ({len(docs)} files)")
            print("-" * 70)

            for doc in sorted(docs, key=lambda d: d.filename):
                # Filter by sync status
                if doc.synced and not show_synced:
                    continue
                if not doc.synced and not show_unsynced:
                    continue

                status = "✅" if doc.synced else "⏳"
                print(f"\n{status} {doc.title or doc.filename}")
                print(f"   File: {doc.filename}")
                print(f"   Path: {doc.path}")
                print(f"   Slug: {doc.slug}")

                if doc.feature_date:
                    print(f"   Date: {doc.feature_date}")

                if doc.synced:
                    print(f"   Synced: {doc.sync_provider} ({doc.sync_date or 'unknown date'})")
                    if doc.public_url:
                        print(f"   URL: {doc.public_url}")
                else:
                    print(f"   Status: Not synced to any KB provider")

        print("\n" + "=" * 70 + "\n")

    def export_json(self, output_path: str):
        """Export inventory to JSON"""
        data = {
            'scanned_at': datetime.now().isoformat(),
            'total_documents': len(self.documents),
            'categories': self.get_categories(),
            'documents': [doc.to_dict() for doc in self.documents]
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Inventory exported to: {output_path}")


def scan_documentation(base_paths: List[str] = None, verbose: bool = True) -> List[DocumentInfo]:
    """
    Convenience function to scan documentation

    Args:
        base_paths: Optional list of paths to scan
        verbose: Whether to print output

    Returns:
        List of DocumentInfo objects
    """
    inventory = DocumentInventory(base_paths)
    documents = inventory.scan()

    if verbose:
        inventory.print_summary()

    return documents


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Scan and catalog documentation'
    )
    parser.add_argument(
        '--paths',
        nargs='+',
        help='Paths to scan (defaults to config paths)'
    )
    parser.add_argument(
        '--category',
        help='Filter by category'
    )
    parser.add_argument(
        '--synced',
        action='store_true',
        help='Show only synced documents'
    )
    parser.add_argument(
        '--unsynced',
        action='store_true',
        help='Show only unsynced documents'
    )
    parser.add_argument(
        '--details',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--export',
        help='Export inventory to JSON file'
    )

    args = parser.parse_args()

    # Scan documentation
    inventory = DocumentInventory(args.paths)
    inventory.scan()

    # Filter by category
    if args.category:
        inventory.documents = inventory.filter_by_category(args.category)

    # Filter by sync status
    if args.synced and not args.unsynced:
        inventory.documents = inventory.filter_synced(True)
    elif args.unsynced and not args.synced:
        inventory.documents = inventory.filter_synced(False)

    # Print output
    if args.details:
        show_synced = not args.unsynced or args.synced
        show_unsynced = not args.synced or args.unsynced
        inventory.print_details(show_synced=show_synced, show_unsynced=show_unsynced)
    else:
        inventory.print_summary()

    # Export if requested
    if args.export:
        inventory.export_json(args.export)
