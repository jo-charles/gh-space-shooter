"""Base class for output format providers."""

from abc import ABC, abstractmethod
from typing import Iterator
from PIL import Image


class OutputProvider(ABC):
    """Abstract base class for output format providers."""

    def __init__(self, fps: int, watermark: bool = False):
        """
        Initialize provider.

        Args:
            fps: Frames per second for the animation
            watermark: Whether to add watermark (available for subclasses)
        """
        self.fps = fps
        self.watermark = watermark
        self.frame_duration = 1000 // fps

    @abstractmethod
    def encode(self, frames: Iterator[Image.Image]) -> bytes:
        """
        Encode frames into the output format.

        Args:
            frames: Iterator of PIL Images

        Returns:
            Encoded output as bytes
        """
        pass
