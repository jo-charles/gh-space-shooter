"""Base Drawable interface for game objects."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PIL import ImageDraw

if TYPE_CHECKING:
    from .render_context import RenderContext


class Drawable(ABC):
    """Interface for objects that can be animated and drawn."""

    @abstractmethod
    def animate(self) -> None:
        """Update the object's state for the next animation frame."""
        pass

    @abstractmethod
    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """
        Draw the object on the image.

        Args:
            draw: PIL ImageDraw object
            context: Rendering context with helper functions and constants
        """
        pass
