#!/usr/bin/env python3
"""
Generic Knowledge Base Integration Module

Provides provider-agnostic KB operations (sync, upload, etc.)
"""

from scripts.kb.sync import sync_article_from_markdown, sync_multiple_articles
from scripts.kb.upload import upload_image, upload_images_batch, upload_from_metadata_file

__all__ = [
    'sync_article_from_markdown',
    'sync_multiple_articles',
    'upload_image',
    'upload_images_batch',
    'upload_from_metadata_file',
]
