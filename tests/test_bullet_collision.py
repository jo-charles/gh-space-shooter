"""Tests for bullet collision detection logic."""

from gh_space_shooter.game.game_state import GameState
from gh_space_shooter.game.drawables import Bullet, Enemy
from gh_space_shooter.constants import EXPLOSION_MAX_FRAMES_SMALL, EXPLOSION_MAX_FRAMES_LARGE


class TestBulletCollision:
    """Tests for bullet collision detection and behavior."""

    def test_collision_detection_same_x_position(self, default_game_state: GameState) -> None:
        """Test that bullet detects collision when at same x position as enemy."""

        enemy = Enemy(x=5, y=3, health=2, game_state=default_game_state)
        default_game_state.enemies.append(enemy)
        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.0
        default_game_state.bullets.append(bullet)

        hit_enemy = bullet._check_collision()
        assert hit_enemy is enemy

        bullet.animate()
        assert bullet not in default_game_state.bullets

    def test_collision_detection_enemy_above_bullet(self, default_game_state: GameState) -> None:
        """Test that collision is detected when enemy.y >= bullet.y."""

        enemy = Enemy(x=5, y=3, health=2, game_state=default_game_state)
        default_game_state.enemies.append(enemy)
        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.5
        default_game_state.bullets.append(bullet)

        hit_enemy = bullet._check_collision()
        assert hit_enemy is enemy

        bullet.animate()
        assert bullet not in default_game_state.bullets

    def test_no_collision_different_x_position(self, default_game_state: GameState) -> None:
        """Test that bullet doesn't detect collision at different x positions."""

        enemy = Enemy(x=5, y=3, health=2, game_state=default_game_state)
        default_game_state.enemies.append(enemy)

        bullet = Bullet(x=6, game_state=default_game_state)
        bullet.y = 3.0

        hit_enemy = bullet._check_collision()
        assert hit_enemy is None

    def test_bullet_damages_enemy_on_collision(self, default_game_state: GameState) -> None:
        """Test that bullet damages enemy on collision."""

        enemy = Enemy(x=5, y=3, health=3, game_state=default_game_state)
        default_game_state.enemies.append(enemy)

        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.0
        default_game_state.bullets.append(bullet)

        bullet.animate()
        assert enemy.health == 2

    def test_enemy_destroyed_when_health_zero(self, default_game_state: GameState) -> None:
        """Test that enemy is removed when health reaches zero."""

        enemy = Enemy(x=5, y=3, health=1, game_state=default_game_state)
        default_game_state.enemies.append(enemy)

        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.0
        default_game_state.bullets.append(bullet)

        bullet.animate()
        assert enemy not in default_game_state.enemies

    def test_explosion_created_on_collision(self, default_game_state: GameState) -> None:
        """Test that explosion is created when bullet hits enemy."""

        enemy = Enemy(x=5, y=3, health=2, game_state=default_game_state)
        default_game_state.enemies.append(enemy)

        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.0
        default_game_state.bullets.append(bullet)

        bullet.animate()
        assert len(default_game_state.explosions) == 1
        assert default_game_state.explosions[0].max_frames == EXPLOSION_MAX_FRAMES_SMALL

    def test_large_explosion_on_enemy_destroyed(self, default_game_state: GameState) -> None:
        """Test that large explosion is created when enemy is destroyed."""

        enemy = Enemy(x=5, y=3, health=1, game_state=default_game_state)
        default_game_state.enemies.append(enemy)

        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = 2.0
        default_game_state.bullets.append(bullet)

        bullet.animate()
        # Should have 2 explosions: small from bullet hit, large from enemy destruction
        assert len(default_game_state.explosions) == 2
        explosion_max_frames = [exp.max_frames for exp in default_game_state.explosions]
        assert EXPLOSION_MAX_FRAMES_SMALL in explosion_max_frames
        assert EXPLOSION_MAX_FRAMES_LARGE in explosion_max_frames

    def test_bullet_removed_when_off_screen(self, default_game_state: GameState) -> None:
        """Test that bullet is removed when it goes off screen (y < -10)."""

        bullet = Bullet(x=5, game_state=default_game_state)
        bullet.y = -5.0
        default_game_state.bullets.append(bullet)

        for _ in range(50):
            if bullet in default_game_state.bullets:
                bullet.animate()

        assert bullet not in default_game_state.bullets
