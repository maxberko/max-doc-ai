#!/usr/bin/env python3
"""
Sync documentation articles to Pylon Knowledge Base

This module handles creating and updating articles in Pylon, including:
- Converting markdown to HTML
- Wrapping images in React components
- Managing article state
- Handling collections
"""

import os
import json
import requests
import sys
from pathlib import Path
from typing import Dict, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
import config as cfg
from pylon import converter
from utils import state as state_manager


class PylonSync:
    """Handles syncing documentation to Pylon Knowledge Base"""

    def __init__(self, api_key=None, kb_id=None, author_id=None):
        """
        Initialize Pylon sync

        Args:
            api_key: Pylon API key (default: from config)
            kb_id: Pylon Knowledge Base ID (default: from config)
            author_id: Pylon author user ID (default: from config)
        """
        pylon_config = cfg.get_pylon_config()

        self.api_key = api_key or pylon_config['api_key']
        self.kb_id = kb_id or pylon_config['kb_id']
        self.author_id = author_id or pylon_config['author_user_id']
        self.base_url = pylon_config['api_base']
        self.collections = pylon_config['collections']

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def create_article(
        self,
        title: str,
        slug: str,
        body_html: str,
        collection_name: str,
        is_published: bool = True
    ) -> Optional[Dict]:
        """
        Create a new article in Pylon

        IMPORTANT: collection_id MUST be set during article creation.
        It cannot be reliably added later via PATCH requests.

        Args:
            title: Article title
            slug: Article slug (URL-friendly identifier)
            body_html: Article HTML content (with React wrappers for images)
            collection_name: Collection name (must match config.yaml)
            is_published: Whether to publish immediately (default: True)

        Returns:
            Dict with article data including URLs, or None if failed
        """
        collection_id = self.collections.get(collection_name)
        if not collection_id:
            print(f"❌ Collection '{collection_name}' not found in config")
            print(f"   Available collections: {list(self.collections.keys())}")
            return None

        print(f"✨ Creating new article: {title}")
        print(f"   Collection: {collection_name} ({collection_id})")

        payload = {
            'title': title,
            'slug': slug,
            'body_html': body_html,
            'author_user_id': self.author_id,
            'collection_id': collection_id,  # CRITICAL: Must be set here!
            'is_published': is_published,
            'publish_updated_body_html': True
        }

        try:
            response = requests.post(
                f'{self.base_url}/knowledge-bases/{self.kb_id}/articles',
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                result = response.json()
                article_data = result.get('data', {})
                article_id = article_data.get('id')

                print(f"   ✅ Created article ID: {article_id}")

                # Extract URLs
                public_url = article_data.get('public_url')
                internal_url = f'https://app.usepylon.com/docs/{self.kb_id}/articles/{article_id}'

                return {
                    'article_id': article_id,
                    'collection_id': collection_id,
                    'public_url': public_url,
                    'internal_url': internal_url,
                    'title': title,
                    'slug': slug
                }
            else:
                print(f"   ❌ Failed to create article: {response.status_code}")
                print(f"      Response: {response.text}")
                return None

        except Exception as e:
            print(f"   ❌ Error creating article: {e}")
            return None

    def update_article(
        self,
        article_id: str,
        body_html: str,
        title: Optional[str] = None
    ) -> bool:
        """
        Update an existing article in Pylon

        Args:
            article_id: Pylon article ID
            body_html: Updated HTML content
            title: Updated title (optional)

        Returns:
            True if successful, False otherwise
        """
        print(f"📝 Updating article: {article_id}")

        payload = {
            'body_html': body_html,
            'publish_updated_body_html': True
        }

        if title:
            payload['title'] = title

        try:
            response = requests.patch(
                f'{self.base_url}/knowledge-bases/{self.kb_id}/articles/{article_id}',
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                print(f"   ✅ Article updated successfully")
                return True
            else:
                print(f"   ❌ Failed to update article: {response.status_code}")
                print(f"      Response: {response.text}")
                return False

        except Exception as e:
            print(f"   ❌ Error updating article: {e}")
            return False

    def sync_article_from_markdown(
        self,
        markdown_path: str,
        article_key: str,
        title: str,
        slug: str,
        collection_name: str
    ) -> Optional[Dict]:
        """
        Sync an article from a markdown file to Pylon

        This handles the complete workflow:
        1. Read markdown file
        2. Convert to HTML with React wrappers
        3. Create or update article in Pylon
        4. Update state tracking

        Args:
            markdown_path: Path to markdown file
            article_key: Unique key for state tracking
            title: Article title
            slug: Article slug
            collection_name: Collection name

        Returns:
            Dict with article info, or None if failed
        """
        print(f"\n{'='*60}")
        print(f"📄 Syncing: {Path(markdown_path).name}")
        print(f"{'='*60}")

        # Read markdown
        if not os.path.exists(markdown_path):
            print(f"❌ File not found: {markdown_path}")
            return None

        with open(markdown_path, 'r') as f:
            md_content = f.read()

        # Convert to HTML with React wrappers
        print("🔄 Converting markdown to HTML...")
        html_content = converter.markdown_to_html_with_react_images(md_content)

        # Validate React wrappers
        is_valid, img_count, msg = converter.validate_react_wrappers(html_content)
        if img_count > 0:
            print(f"   {'✅' if is_valid else '❌'} {msg}")

        # Load state to check if article exists
        state_data = state_manager.load_state()
        existing_article = state_data.get('articles', {}).get(article_key)

        if existing_article and existing_article.get('article_id'):
            # Update existing article
            article_id = existing_article['article_id']
            success = self.update_article(article_id, html_content, title)

            if success:
                # Update state with new sync time
                state_manager.update_article_sync_time(article_key)
                return existing_article
            else:
                return None
        else:
            # Create new article
            article_data = self.create_article(
                title=title,
                slug=slug,
                body_html=html_content,
                collection_name=collection_name
            )

            if article_data:
                # Save to state
                state_manager.save_article(article_key, article_data)
                return article_data
            else:
                return None


def sync_documentation_category(category: str, articles: List[Dict]) -> Dict[str, Dict]:
    """
    Sync all articles in a documentation category

    Args:
        category: Category name (must match config.yaml)
        articles: List of article dicts with 'key', 'file', 'title', 'slug'

    Returns:
        Dict mapping article keys to sync results
    """
    syncer = PylonSync()
    results = {}

    print(f"\n{'='*60}")
    print(f"🚀 Syncing category: {category}")
    print(f"{'='*60}")

    docs_base = cfg.get_documentation_config()['base_path']

    for article in articles:
        article_key = article['key']
        article_file = article['file']
        title = article['title']
        slug = article['slug']

        # Construct full path
        markdown_path = os.path.join(docs_base, article_file)

        # Sync
        result = syncer.sync_article_from_markdown(
            markdown_path=markdown_path,
            article_key=article_key,
            title=title,
            slug=slug,
            collection_name=category
        )

        results[article_key] = result

    # Summary
    success_count = sum(1 for r in results.values() if r is not None)
    print(f"\n{'='*60}")
    print(f"✅ Synced {success_count}/{len(articles)} articles in {category}")
    print(f"{'='*60}\n")

    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync documentation articles to Pylon'
    )
    parser.add_argument(
        '--file',
        help='Markdown file to sync'
    )
    parser.add_argument(
        '--key',
        help='Article key for state tracking (required with --file)'
    )
    parser.add_argument(
        '--title',
        help='Article title (required with --file)'
    )
    parser.add_argument(
        '--slug',
        help='Article slug (required with --file)'
    )
    parser.add_argument(
        '--collection',
        help='Collection name (required with --file)'
    )

    args = parser.parse_args()

    if args.file:
        # Sync single file
        if not all([args.key, args.title, args.slug, args.collection]):
            print("❌ When using --file, you must provide: --key, --title, --slug, --collection")
            sys.exit(1)

        syncer = PylonSync()
        result = syncer.sync_article_from_markdown(
            markdown_path=args.file,
            article_key=args.key,
            title=args.title,
            slug=args.slug,
            collection_name=args.collection
        )

        if result:
            print(f"\n✅ Article synced successfully!")
            print(f"   Public URL: {result.get('public_url')}")
            print(f"   Internal URL: {result.get('internal_url')}")
        else:
            print("\n❌ Sync failed")
            sys.exit(1)
    else:
        print("ℹ️  Pylon Sync Tool")
        print("\nUsage:")
        print("  python3 sync.py --file FILE --key KEY --title TITLE --slug SLUG --collection COLLECTION")
        print("\nExample:")
        print("  python3 sync.py \\")
        print("    --file demo/docs/product_documentation/features/dashboards.md \\")
        print("    --key dashboards \\")
        print("    --title 'Dashboards' \\")
        print("    --slug 'dashboards' \\")
        print("    --collection features")
