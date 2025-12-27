#!/usr/bin/env python3
"""
Pylon Knowledge Base Provider

Implements the KBProvider interface for Pylon.
"""

import os
import requests
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from utils.kb_providers.base import KBProvider, Article, ImageUpload, ArticleStatus
from pylon import converter as pylon_converter


class PylonProvider(KBProvider):
    """Pylon-specific implementation of KBProvider"""

    def __init__(self, config: Dict):
        """
        Initialize Pylon provider

        Args:
            config: Dict with keys:
                - api_key: Pylon API key
                - kb_id: Knowledge base ID
                - author_user_id: Default author ID
                - api_base: Base URL (default: https://api.usepylon.com)
                - collections: Dict mapping collection names to IDs
        """
        self.api_key = config['api_key']
        self.kb_id = config['kb_id']
        self.author_id = config.get('author_user_id')
        self.base_url = config.get('api_base', 'https://api.usepylon.com')
        self.collections = config.get('collections', {})

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    @property
    def provider_name(self) -> str:
        return "pylon"

    # Article Management

    def create_article(self, article: Article) -> Optional[Article]:
        """
        Create a new article in Pylon

        IMPORTANT: collection_id MUST be set during article creation.
        """
        collection_id = article.collection_id
        if not collection_id and article.collection_name:
            collection_id = self.get_collection_id(article.collection_name)

        if not collection_id:
            print(f"❌ Collection not specified for article: {article.title}")
            return None

        print(f"✨ Creating new article: {article.title}")
        print(f"   Collection: {article.collection_name or 'Unknown'} ({collection_id})")

        payload = {
            'title': article.title,
            'slug': article.slug,
            'body_html': article.body_html,
            'author_user_id': article.author_id or self.author_id,
            'collection_id': collection_id,  # CRITICAL: Must be set here!
            'is_published': article.status == ArticleStatus.PUBLISHED,
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

                # Update article with response data
                article.id = article_id
                article.collection_id = collection_id
                article.public_url = article_data.get('public_url')
                article.internal_url = f'https://app.usepylon.com/docs/{self.kb_id}/articles/{article_id}'

                return article
            else:
                print(f"   ❌ Failed to create article: {response.status_code}")
                print(f"      Response: {response.text}")
                return None

        except Exception as e:
            print(f"   ❌ Error creating article: {e}")
            return None

    def update_article(self, article_id: str, article: Article) -> bool:
        """Update an existing article in Pylon"""
        print(f"📝 Updating article: {article_id}")

        payload = {
            'body_html': article.body_html,
            'publish_updated_body_html': True
        }

        if article.title:
            payload['title'] = article.title

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

    def get_article(self, article_id: str) -> Optional[Article]:
        """Retrieve an article by ID"""
        try:
            response = requests.get(
                f'{self.base_url}/knowledge-bases/{self.kb_id}/articles/{article_id}',
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json().get('data', {})
                return self._parse_article_data(data)
            else:
                print(f"❌ Failed to get article: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error getting article: {e}")
            return None

    def delete_article(self, article_id: str) -> bool:
        """Delete an article"""
        try:
            response = requests.delete(
                f'{self.base_url}/knowledge-bases/{self.kb_id}/articles/{article_id}',
                headers=self.headers
            )

            if response.status_code in [200, 204]:
                print(f"✅ Article deleted: {article_id}")
                return True
            else:
                print(f"❌ Failed to delete article: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error deleting article: {e}")
            return False

    def list_articles(self, collection_id: Optional[str] = None) -> List[Article]:
        """
        List all articles

        Note: Pylon's API doesn't provide a list endpoint,
        so this method requires maintaining state externally.
        """
        print("⚠️  Pylon doesn't provide a list articles endpoint")
        print("   Use state file to track articles")
        return []

    # Image/Attachment Management

    def upload_image(self, image_path: str, alt_text: str = "", caption: str = "") -> Optional[ImageUpload]:
        """Upload an image to Pylon's Attachments API"""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None

        print(f"📤 Uploading: {Path(image_path).name}...")

        filename = Path(image_path).name
        with open(image_path, 'rb') as f:
            files = {
                'file': (filename, f, f'image/{Path(image_path).suffix[1:]}')
            }

            data = {}
            if alt_text:
                data['alt_text'] = alt_text
            if caption:
                data['caption'] = caption

            url = f'{self.base_url}/attachments'

            try:
                response = requests.post(
                    url,
                    headers={'Authorization': f'Bearer {self.api_key}'},
                    files=files,
                    data=data
                )

                if response.status_code in [200, 201]:
                    result = response.json()
                    image_url = result.get('data', {}).get('url')

                    if image_url:
                        print(f"   ✅ Uploaded: {image_url}")
                        return ImageUpload(
                            url=image_url,
                            filename=filename,
                            alt_text=alt_text,
                            caption=caption,
                            provider_id=result.get('data', {}).get('id')
                        )
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

    def upload_images_batch(self, images: List[Dict]) -> Dict[str, ImageUpload]:
        """Upload multiple screenshots"""
        results = {}

        print(f"\n📤 Uploading {len(images)} images to Pylon...\n")

        for img in images:
            name = img.get('name')
            path = img.get('path')
            alt_text = img.get('alt', '')
            caption = img.get('caption', '')

            result = self.upload_image(path, alt_text, caption)

            if result:
                results[name] = result
            else:
                print(f"   ⚠️  Skipping {name} due to upload failure")

        print(f"\n✅ Successfully uploaded {len(results)}/{len(images)} images")

        return results

    # Content Conversion

    def markdown_to_html(self, markdown: str) -> str:
        """
        Convert markdown to Pylon-specific HTML

        Pylon requires images to be wrapped in React component structures.
        """
        return pylon_converter.markdown_to_html_with_react_images(markdown)

    def validate_html(self, html: str) -> tuple[bool, str]:
        """Validate that HTML has proper React wrappers for images"""
        is_valid, img_count, msg = pylon_converter.validate_react_wrappers(html)
        return is_valid, msg

    # Collections/Categories

    def get_collection_id(self, collection_name: str) -> Optional[str]:
        """Get collection ID from collection name"""
        return self.collections.get(collection_name)

    def list_collections(self) -> List[Dict]:
        """List all configured collections"""
        return [
            {'id': coll_id, 'name': name}
            for name, coll_id in self.collections.items()
        ]

    # Utility Methods

    def test_connection(self) -> bool:
        """Test the connection to Pylon"""
        try:
            response = requests.get(
                f'{self.base_url}/knowledge-bases/{self.kb_id}',
                headers=self.headers
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

    def _parse_article_data(self, data: Dict) -> Article:
        """Parse Pylon API response into Article object"""
        return Article(
            id=data.get('id'),
            title=data.get('title', ''),
            slug=data.get('slug', ''),
            body_html=data.get('body_html', ''),
            status=ArticleStatus.PUBLISHED if data.get('is_published') else ArticleStatus.DRAFT,
            collection_id=data.get('collection_id'),
            public_url=data.get('public_url'),
            internal_url=f'https://app.usepylon.com/docs/{self.kb_id}/articles/{data.get("id")}',
            author_id=data.get('author_user_id'),
            metadata=data
        )
