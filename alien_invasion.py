import sys
from time import sleep

import pygame, math

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # ryan: i added a lot of args, check ship.py for arg names
        self.player1 = Ship(self, 'images/ship.bmp', (self.settings.screen_width // 2, self.settings.screen_height - 100), math.pi, (192, 192, 192))
        self.player2 = Ship(self, 'images/ship2.png', (self.settings.screen_width // 2, 100), 0, (0, 0, 0))
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        """self._create_fleet()"""

        # Set controls for player 1 and player 2.
        self.p1turn = pygame.K_RIGHT
        self.p1shoot = pygame.K_DOWN
        self.p2turn = pygame.K_s
        self.p2shoot = pygame.K_a

        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.player1.update()
                self.player2.update()
                self._update_bullets()
                # self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == self.p1turn:
            self.player1.turning = True
        if event.key == self.p1shoot:
            self._fire_bullet(self.player1)
        if event.key == self.p2turn:
            self.player2.turning = True
        if event.key == self.p2shoot:
            self._fire_bullet(self.player2)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == self.p1turn:
            self.player1.turning = False
        if event.key == self.p2turn:
            self.player2.turning = False

    def _fire_bullet(self, ship):
        """Create a new bullet and add it to the bullets group."""
        if ship.bullets_active < self.settings.bullets_allowed:
            ship.bullets_active += 1
            self.bullets.add(Bullet(self, ship))

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen.get_rect().bottom or bullet.rect.left <= 0 or bullet.rect.right >= self.screen.get_rect().right:
                bullet.owner.bullets_active -= 1
                self.bullets.remove(bullet)

        # self._check_bullet_alien_collisions()
        

    # def _check_bullet_alien_collisions(self):
    #     """Respond to bullet-alien collisions."""
    #     # Remove any bullets and aliens that have collided.
    #     collisions = pygame.sprite.groupcollide(
    #             self.bullets, self.aliens, True, True)

    #     if not self.aliens:
    #         # Destroy existing bullets and create new fleet.
    #         self.bullets.empty()
    #         self._create_fleet()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            # self._create_fleet()
            self.player1.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.player1.blitme()
        self.player2.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
