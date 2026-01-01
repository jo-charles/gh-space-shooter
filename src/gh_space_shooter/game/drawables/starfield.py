"""Animated starfield background."""

import random
from typing import TYPE_CHECKING

from PIL import ImageDraw

from ...constants import NUM_WEEKS, SHIP_POSITION_Y
from .drawable import Drawable

if TYPE_CHECKING:
    from ..render_context import RenderContext


class Starfield(Drawable):
    """Animated starfield background with slowly moving stars."""

    def __init__(self):
        """Initialize the starfield with random stars."""
        self.stars = []
        # Generate about 100 stars across the play area
        for _ in range(100):
            # Random position across the entire grid area
            x = random.uniform(-2, NUM_WEEKS + 2)
            y = random.uniform(-2, SHIP_POSITION_Y + 4)
            # Brightness: 0.2 to 1.0 (dimmer stars for depth)
            brightness = random.uniform(0.2, 1.0)
            # Size: 1-2 pixels
            size = random.choice([1, 1, 1, 2])  # More 1-pixel stars
            # Speed: slower for dimmer (farther) stars
            speed = 0.02 + (brightness * 0.03)  # 0.02-0.05 cells per frame
            self.stars.append([x, y, brightness, size, speed])

    def animate(self) -> None:
        """Move stars downward, wrapping around when they go off screen."""
        for star in self.stars:
            # star[1] is the y position, star[4] is the speed
            star[1] += star[4]

            # Wrap around: if star goes below the screen, move it back to the top
            if star[1] > SHIP_POSITION_Y + 4:
                star[1] = -2
                # Randomize x position when wrapping for variety
                star[0] = random.uniform(-2, NUM_WEEKS + 2)

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw all stars at their current positions."""
        for star_x, star_y, brightness, size, _ in self.stars:
            # Convert grid position to pixel position
            x, y = context.get_cell_position(star_x, star_y)

            # Calculate star color (white with varying brightness)
            star_brightness = int(255 * brightness)
            star_color = (star_brightness, star_brightness, star_brightness, 255)

            # Draw star as a small rectangle or point
            if size == 1:
                # Single pixel star
                draw.point([(x, y)], fill=star_color)
            else:
                # Slightly larger star (2x2)
                draw.rectangle(
                    [x, y, x + size - 1, y + size - 1],
                    fill=star_color
                )
