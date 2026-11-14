import pygame
import math
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.owner = ship
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ship.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        """
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop"""
        base_image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height), pygame.SRCALPHA)
        base_image.fill(self.color)

        # set direction
        self.direction = ship.direction

        # make bullet face direction
        self.image = pygame.transform.rotate(base_image, -math.degrees(ship.direction))

        # 4. Position the bullet at the ship's midpoint/firing point
        self.rect = self.image.get_rect()
        self.rect.center = ship.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y += self.settings.bullet_speed * math.cos(self.direction)
        self.x += self.settings.bullet_speed * math.sin(self.direction)
        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
