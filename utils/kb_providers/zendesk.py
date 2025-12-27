#!/usr/bin/env python3
"""
Zendesk Guide Provider (Example Implementation)

Implements the KBProvider interface for Zendesk Guide.
This is an example/template - adjust based on actual Zendesk API.
"""

import os
import requests
from pathlib import Path
from typing import Dict, List, Optional
import markdown

from utils.kb_providers.base import KBProvider, Article, ImageUpload, ArticleStatus


class ZendeskProvider(KBProvider):
    """Zendesk Guide implementation of KBProvider"""

    def __init__(self, config: Dict):
        """
        Initialize Zendesk provider

        Args:
            config: Dict with keys:
                - subdomain: Zendesk subdomain (e.g., 'mycompany')
                - email: Admin email
                - api_token: API token
                - brand_id: Brand ID (optional)
                - locale: Default locale (default: 'en-us')
                - categories: Dict mapping category names to IDs
        """
        self.subdomain = config['subdomain']
        self.email = config['email']
        self.api_token = config['api_token']
        self.brand_id = config.get('brand_id')
        self.locale = config.get('locale', 'en-us')
        self.categories = config.get('categories', {})

        self.base_url = f'https://{self.subdomain}.zendesk.com/api/v2/help_center'
        self.auth = (f'{self.email}/token', self.api_token)

    @property
    def provider_name(self) -> str:
        return "zendesk"

    # Article Management

    def create_article(self, article: Article) -> Optional[Article]:
        """Create a new article in Zendesk Guide"""
        section_id = article.collection_id
        if not section_id and article.collection_name:
            section_id = self.get_collection_id(article.collection_name)

        if not section_id:
            print(f"❌ Section not specified for article: {article.title}")
            return None

        print(f"✨ Creating new article: {article.title}")
        print(f"   Section: {article.collection_name or 'Unknown'} ({section_id})")

        payload = {
            'article': {
                'title': article.title,
                'body': article.body_html,
                'locale': self.locale,
                'draft': article.status == ArticleStatus.DRAFT,
                'user_segment_id': None  # Visible to all users
            }
        }

        try:
            response = requests.post(
                f'{self.base_url}/{self.locale}/sections/{section_id}/articles.json',
                auth=self.auth,
                json=payload
            )

            if response.status_code in [200, 201]:
                result = response.json()
                article_data = result.get('article', {})
                article_id = article_data.get('id')

                print(f"   ✅ Created article ID: {article_id}")

                # Update article with response data
                article.id = str(article_id)
                article.collection_id = section_id
                article.public_url = article_data.get('html_url')
                article.internal_url = f'https://{self.subdomain}.zendesk.com/hc/admin/articles/{article_id}'

                return article
            else:
                print(f"   ❌ Failed to create article: {response.status_code}")
                print(f"      Response: {response.text}")
                return None

        except Exception as e:
            print(f"   ❌ Error creating article: {e}")
            return None

    def update_article(self, article_id: str, article: Article) -> bool:
        """Update an existing article in Zendesk Guide"""
        print(f"📝 Updating article: {article_id}")

        payload = {
            'article': {
                'body': article.body_html
            }
        }

        if article.title:
            payload['article']['title'] = article.title

        try:
            response = requests.put(
                f'{self.base_url}/articles/{article_id}/translations/{self.locale}.json',
                auth=self.auth,
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
                f'{self.base_url}/articles/{article_id}.json',
                auth=self.auth
            )

            if response.status_code == 200:
                data = response.json().get('article', {})
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
                f'{self.base_url}/articles/{article_id}.json',
                auth=self.auth
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
        """List all articles in a section"""
        try:
            if collection_id:
                url = f'{self.base_url}/sections/{collection_id}/articles.json'
            else:
                url = f'{self.base_url}/articles.json'

            response = requests.get(url, auth=self.auth)

            if response.status_code == 200:
                articles_data = response.json().get('articles', [])
                return [self._parse_article_data(data) for data in articles_data]
            else:
                print(f"❌ Failed to list articles: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error listing articles: {e}")
            return []

    # Image/Attachment Management

    def upload_image(self, image_path: str, alt_text: str = "", caption: str = "") -> Optional[ImageUpload]:
        """Upload an image to Zendesk"""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None

        print(f"📤 Uploading: {Path(image_path).name}...")

        filename = Path(image_path).name

        # Create an article attachment (requires article ID, so this is simplified)
        # In practice, you'd need to handle inline vs attached images differently
        with open(image_path, 'rb') as f:
            files = {
                'inline': (filename, f, f'image/{Path(image_path).suffix[1:]}')
            }

            try:
                # This is a simplified version - actual implementation depends on use case
                response = requests.post(
                    f'{self.base_url}/articles/attachments.json',
                    auth=self.auth,
                    files=files
                )

                if response.status_code in [200, 201]:
                    result = response.json()
                    attachment = result.get('article_attachment', {})
                    image_url = attachment.get('content_url')

                    if image_url:
                        print(f"   ✅ Uploaded: {image_url}")
                        return ImageUpload(
                            url=image_url,
                            filename=filename,
                            alt_text=alt_text,
                            caption=caption,
                            provider_id=str(attachment.get('id'))
                        )
                    else:
                        print(f"   ⚠️  No URL in response")
                        return None
                else:
                    print(f"   ❌ Upload failed: {response.status_code}")
                    return None

            except Exception as e:
                print(f"   ❌ Error uploading: {e}")
                return None

    def upload_images_batch(self, images: List[Dict]) -> Dict[str, ImageUpload]:
        """Upload multiple images"""
        results = {}

        print(f"\n📤 Uploading {len(images)} images to Zendesk...\n")

        for img in images:
            name = img.get('name')
            path = img.get('path')
            alt_text = img.get('alt', '')
            caption = img.get('caption', '')

            result = self.upload_image(path, alt_text, caption)

            if result:
                results[name] = result

        print(f"\n✅ Successfully uploaded {len(results)}/{len(images)} images")

        return results

    # Content Conversion

    def markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown to HTML

        Zendesk accepts standard HTML, so we use basic markdown conversion.
        """
        html = markdown.markdown(
            markdown_content,
            extensions=['extra', 'nl2br', 'fenced_code', 'tables']
        )
        return html

    def validate_html(self, html: str) -> tuple[bool, str]:
        """Validate HTML (Zendesk is pretty flexible)"""
        if not html or not html.strip():
            return False, "HTML is empty"
        return True, "HTML looks valid"

    # Collections/Categories

    def get_collection_id(self, collection_name: str) -> Optional[str]:
        """Get section ID from section name"""
        return self.categories.get(collection_name)

    def list_collections(self) -> List[Dict]:
        """List all sections"""
        try:
            response = requests.get(
                f'{self.base_url}/sections.json',
                auth=self.auth
            )

            if response.status_code == 200:
                sections = response.json().get('sections', [])
                return [
                    {
                        'id': str(section['id']),
                        'name': section['name'],
                        'description': section.get('description', '')
                    }
                    for section in sections
                ]
            else:
                return []

        except Exception as e:
            print(f"❌ Error listing sections: {e}")
            return []

    # Utility Methods

    def test_connection(self) -> bool:
        """Test the connection to Zendesk"""
        try:
            response = requests.get(
                f'{self.base_url}/categories.json',
                auth=self.auth
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

    def _parse_article_data(self, data: Dict) -> Article:
        """Parse Zendesk API response into Article object"""
        return Article(
            id=str(data.get('id')),
            title=data.get('title', ''),
            slug=data.get('name', ''),  # Zendesk uses 'name' for slug
            body_html=data.get('body', ''),
            status=ArticleStatus.PUBLISHED if not data.get('draft') else ArticleStatus.DRAFT,
            collection_id=str(data.get('section_id')),
            public_url=data.get('html_url'),
            internal_url=f'https://{self.subdomain}.zendesk.com/hc/admin/articles/{data.get("id")}',
            author_id=str(data.get('author_id')),
            metadata=data
        )
