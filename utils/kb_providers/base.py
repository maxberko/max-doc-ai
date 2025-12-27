#!/usr/bin/env python3
"""
Abstract Base Class for Knowledge Base Providers

Defines the interface that all KB providers must implement.
Supports providers like: Pylon, Zendesk, Confluence, Notion, Intercom, etc.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ArticleStatus(Enum):
    """Article publication status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Article:
    """Generic article representation"""
    id: Optional[str] = None
    title: str = ""
    slug: str = ""
    body_html: str = ""
    status: ArticleStatus = ArticleStatus.PUBLISHED
    collection_id: Optional[str] = None
    collection_name: Optional[str] = None
    public_url: Optional[str] = None
    internal_url: Optional[str] = None
    author_id: Optional[str] = None
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ImageUpload:
    """Generic image upload result"""
    url: str
    filename: str
    alt_text: str = ""
    caption: str = ""
    provider_id: Optional[str] = None
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class KBProvider(ABC):
    """
    Abstract base class for Knowledge Base providers

    All KB providers must implement these methods.
    """

    @abstractmethod
    def __init__(self, config: Dict):
        """
        Initialize the provider with configuration

        Args:
            config: Provider-specific configuration dict
                   Should include: api_key, base_url, etc.
        """
        pass

    # Article Management

    @abstractmethod
    def create_article(self, article: Article) -> Optional[Article]:
        """
        Create a new article in the knowledge base

        Args:
            article: Article object with title, body_html, etc.

        Returns:
            Article object with id and URLs populated, or None if failed
        """
        pass

    @abstractmethod
    def update_article(self, article_id: str, article: Article) -> bool:
        """
        Update an existing article

        Args:
            article_id: Provider's article ID
            article: Article object with updated fields

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_article(self, article_id: str) -> Optional[Article]:
        """
        Retrieve an article by ID

        Args:
            article_id: Provider's article ID

        Returns:
            Article object or None if not found
        """
        pass

    @abstractmethod
    def delete_article(self, article_id: str) -> bool:
        """
        Delete an article

        Args:
            article_id: Provider's article ID

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def list_articles(self, collection_id: Optional[str] = None) -> List[Article]:
        """
        List all articles, optionally filtered by collection

        Args:
            collection_id: Optional collection ID to filter by

        Returns:
            List of Article objects
        """
        pass

    # Image/Attachment Management

    @abstractmethod
    def upload_image(self, image_path: str, alt_text: str = "", caption: str = "") -> Optional[ImageUpload]:
        """
        Upload an image to the provider's CDN/storage

        Args:
            image_path: Path to the image file
            alt_text: Alternative text for accessibility
            caption: Image caption

        Returns:
            ImageUpload object with URL, or None if failed
        """
        pass

    @abstractmethod
    def upload_images_batch(self, images: List[Dict]) -> Dict[str, ImageUpload]:
        """
        Upload multiple images

        Args:
            images: List of dicts with 'path', 'alt', 'caption'

        Returns:
            Dict mapping image names to ImageUpload results
        """
        pass

    # Content Conversion

    @abstractmethod
    def markdown_to_html(self, markdown: str) -> str:
        """
        Convert markdown to provider-specific HTML

        Different providers may require special HTML structures.
        For example, Pylon needs React component wrappers for images.

        Args:
            markdown: Markdown content string

        Returns:
            HTML content ready for the provider
        """
        pass

    @abstractmethod
    def validate_html(self, html: str) -> tuple[bool, str]:
        """
        Validate that HTML meets provider requirements

        Args:
            html: HTML content to validate

        Returns:
            Tuple of (is_valid, message)
        """
        pass

    # Collections/Categories

    @abstractmethod
    def get_collection_id(self, collection_name: str) -> Optional[str]:
        """
        Get collection ID from collection name

        Args:
            collection_name: Human-readable collection name

        Returns:
            Provider's collection ID or None if not found
        """
        pass

    @abstractmethod
    def list_collections(self) -> List[Dict]:
        """
        List all available collections/categories

        Returns:
            List of dicts with 'id', 'name', 'description'
        """
        pass

    # Utility Methods

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'pylon', 'zendesk')"""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test the connection to the provider

        Returns:
            True if connection is working, False otherwise
        """
        pass

    def get_article_urls(self, article: Article) -> Dict[str, str]:
        """
        Get URLs for an article

        Args:
            article: Article object

        Returns:
            Dict with 'public_url' and 'internal_url'
        """
        return {
            'public_url': article.public_url or '',
            'internal_url': article.internal_url or ''
        }
