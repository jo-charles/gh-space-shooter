"""Player ship object."""

from typing import TYPE_CHECKING

from PIL import ImageDraw

from ...constants import SHIP_POSITION_Y, SHIP_SHOOT_COOLDOWN_FRAMES, SHIP_SPEED
from .drawable import Drawable

if TYPE_CHECKING:
    from ..game_state import GameState
    from ..render_context import RenderContext


class Ship(Drawable):
    """Represents the player's ship."""

    def __init__(self, game_state: "GameState"):
        """Initialize the ship at starting position."""
        self.x: float = 25  # Start middle of screen
        self.target_x = self.x
        self.shoot_cooldown = 0  # Frames until ship can shoot again
        self.game_state = game_state

    def move_to(self, x: int):
        """
        Move ship to a new x position.

        Args:
            x: Target x position
        """
        self.target_x = x

    def is_moving(self) -> bool:
        """Check if ship is moving to a new position."""
        return self.x != self.target_x

    def can_shoot(self) -> bool:
        """Check if ship can shoot (cooldown has finished)."""
        return self.shoot_cooldown == 0

    def animate(self) -> None:
        """Update ship position, moving toward target at constant speed."""
        if self.x < self.target_x:
            self.x = min(self.x + SHIP_SPEED, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - SHIP_SPEED, self.target_x)

        # Decrement shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw the ship with gradient effects and detailed design."""
        # Ship stays below the grid at a fixed vertical position
        x, y = context.get_cell_position(self.x, SHIP_POSITION_Y)

        # Calculate ship dimensions
        center_x = x + context.cell_size // 2
        width = context.cell_size
        height = context.cell_size

        # Extract base color components
        r, g, b = context.ship_color

        # Draw engine glow (bottom, brightest)
        glow_color = (min(r + 40, 255), min(g + 40, 255), min(b + 60, 255))
        draw.ellipse(
            [center_x - 3, y + height - 4, center_x + 3, y + height + 2],
            fill=glow_color
        )

        # Draw wings (darker shade)
        wing_color = (max(r - 30, 0), max(g - 30, 0), max(b - 30, 0))
        # Left wing
        draw.polygon(
            [
                (center_x - 2, y + height * 0.4),
                (x - 2, y + height * 0.7),
                (x + 2, y + height * 0.8),
            ],
            fill=wing_color
        )
        # Right wing
        draw.polygon(
            [
                (center_x + 2, y + height * 0.4),
                (x + width + 2, y + height * 0.7),
                (x + width - 2, y + height * 0.8),
            ],
            fill=wing_color
        )

        # Draw main body with gradient (3 segments for smooth gradient)
        # Front segment (lightest)
        front_color = (min(r + 30, 255), min(g + 30, 255), min(b + 40, 255))
        draw.polygon(
            [
                (center_x, y),  # Nose
                (center_x - 4, y + height * 0.35),
                (center_x + 4, y + height * 0.35),
            ],
            fill=front_color
        )

        # Middle segment (base color)
        draw.polygon(
            [
                (center_x - 4, y + height * 0.35),
                (center_x + 4, y + height * 0.35),
                (center_x - 5, y + height * 0.7),
                (center_x + 5, y + height * 0.7),
            ],
            fill=context.ship_color
        )

        # Back segment (darker)
        back_color = (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))
        draw.polygon(
            [
                (center_x - 5, y + height * 0.7),
                (center_x + 5, y + height * 0.7),
                (center_x - 4, y + height),
                (center_x + 4, y + height),
            ],
            fill=back_color
        )

        # Draw cockpit (bright accent)
        cockpit_color = (min(r + 80, 255), min(g + 100, 255), min(b + 120, 255))
        draw.ellipse(
            [center_x - 2, y + height * 0.25, center_x + 2, y + height * 0.45],
            fill=cockpit_color
        )
