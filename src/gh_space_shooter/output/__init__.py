"""Output providers for different animation formats."""

from .base import OutputProvider
from .gif_provider import GifOutputProvider
from .webp_provider import WebPOutputProvider

__all__ = ["OutputProvider", "GifOutputProvider", "WebPOutputProvider"]
