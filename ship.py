import pygame
import math


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game, image_path, center, direction, bullet_color):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.og_image = pygame.image.load(image_path).convert_alpha()
        self.start_center = center
        self.start_direction = direction
        self.turning = False
        self.bullets_active = 0
        self.bullet_color = bullet_color
        self.center_ship()

    def center_ship(self):
        """Centers ship on screen."""
        self.direction = self.start_direction
        self.image = pygame.transform.rotate(self.og_image, 180 + 180 * self.direction / math.pi)
        self.rect = self.image.get_rect(center=self.start_center)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.


        if self.turning:
            self.direction += self.settings.ship_turn_speed
            self.image = pygame.transform.rotate(self.og_image, 180+180*self.direction/math.pi)

        yspeed = self.settings.ship_speed * math.cos(self.direction)
        xspeed = self.settings.ship_speed * math.sin(self.direction)

        if xspeed > 0 and self.rect.right < self.screen_rect.right or xspeed < 0 and self.rect.left > 0:
            self.x += xspeed
        if yspeed > 0 and self.rect.bottom < self.screen_rect.bottom or yspeed < 0 and self.rect.top > 0:
            self.y += yspeed
            
        # Update rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
