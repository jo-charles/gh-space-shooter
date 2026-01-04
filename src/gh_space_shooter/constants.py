"""Global constants for the application."""

# GitHub contribution graph dimensions
NUM_WEEKS = 52  # Number of weeks in contribution graph
NUM_DAYS = 7  # Number of days in a week (Sun-Sat)
SHIP_POSITION_Y = NUM_DAYS + 3  # Ship is positioned just below the grid

SHIP_SPEED = 0.25  # Cells per frame the ship moves
BULLET_SPEED = 0.15  # Cells per frame the bullet moves
BULLET_TRAILING_LENGTH = 3  # Number of trailing segments for bullets
FRAME_DURATION_MS = 20  # Duration of each frame in milliseconds
SHIP_SHOOT_COOLDOWN_FRAMES = 10  # Frames between ship shots

EXPLOSION_PARTICLE_COUNT_LARGE = 8  # Number of particles in a large explosion
EXPLOSION_PARTICLE_COUNT_SMALL = 4  # Number of particles in a small explosion
EXPLOSION_MAX_RADIUS_LARGE = 20  # Max radius for large explosions
EXPLOSION_MAX_RADIUS_SMALL = 10  # Max radius for small explosions
EXPLOSION_MAX_FRAMES_LARGE = 20  # Frames for large explosion animation
EXPLOSION_MAX_FRAMES_SMALL = 6  # Frames for small explosion animation