import sys
from time import sleep

import pygame, math

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.background = pygame.image.load("images/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # ryan: i added a lot of args, check ship.py for arg names
        self.player1 = Ship(self, 'images/ship_rev.png', (self.settings.screen_width // 2, self.settings.screen_height - 100), math.pi, (237, 28, 36))
        self.player2 = Ship(self, 'images/ship2_rev.png', (self.settings.screen_width // 2, 100), 0, (47, 54, 153))
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
        self.winner = None

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.player1.update()
                self.player2.update()
                self._update_bullets()

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
        if event.key == pygame.K_r and self.winner is not None:
            self._restart_game()
            return

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

    def _check_bullet_ship_collisions(self):
        for bullet in list(self.bullets):
            if bullet.owner is self.player1:
                target_ship=self.player2

            elif bullet.owner is self.player2:
                target_ship=self.player1
            else:
                continue

            if bullet.rect.colliderect(target_ship.rect):
                target_ship.hp-=10
                bullet.owner.bullets_active=bullet.owner.bullets_active-1
                self.bullets.remove(bullet)

                if target_ship.hp==0:
                    if target_ship is self.player1:
                        self.winner = "PLAYER 2"
                    else:
                        self.winner = "PLAYER 1"

                    self.game_active = False

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

        self._check_bullet_ship_collisions()
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets.
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self.player1.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False

    def _draw_health_bars(self):
        '''Display for health bars for both ships'''
        bar_width=220
        bar_height=18
        icon_size=42
        margin=20
        top=20

        players = [(self.player1, "PLAYER 1", "left"), 
                    (self.player2, "PLAYER 2", "right"),]

        for ship, label, side in players:
            icon = pygame.transform.smoothscale(ship.og_image, (icon_size, icon_size))

            if side == "left":
                icon_rect = pygame.Rect(margin, top, icon_size, icon_size)
                bar = icon_rect.right+10

            else:
                icon_rect = pygame.Rect(self.settings.screen_width-margin-icon_size, top, icon_size, icon_size)
                bar = icon_rect.left-10-bar_width

            self.screen.blit(icon, icon_rect)

            bar_rect=pygame.Rect(bar, top, bar_width, bar_height)

            health_fraction = ship.hp/ship.max_hp

            fill_rect=bar_rect.copy()
            fill_rect.width = round(bar_width * health_fraction)

            if health_fraction > 0.7:
                health_color=(0,128,0) #green

            elif health_fraction > 0.5:
                health_color=(154, 205, 50) #greenish-yellow

            elif health_fraction > 0.25:
                health_color=(225, 225, 0) #yellow

            else:
                health_color=(225, 0, 0) #red

            if fill_rect.width>0:
                pygame.draw.rect(self.screen, health_color, fill_rect)

            pygame.draw.rect(self.screen, (20,20,20), bar_rect, 2)

    def _draw_winner(self):
        '''Display for victorious player'''
        font = pygame.font.SysFont(None, 100)
        text = font.render(f"{self.winner} WINS", True, (255, 255, 255))
        text_rect=text.get_rect(center=self.screen.get_rect().center)

        self.screen.blit(text, text_rect)

        r_font = pygame.font.SysFont(None, 50)
        r_text = r_font.render(f"Press R to Restart", True, (255, 255, 255))
        r_rect = r_text.get_rect(center=(self.screen.get_rect().centerx, text_rect.bottom+20))

        self.screen.blit(r_text, r_rect)

    def _restart_game(self):
        '''Sets game_active to true and resets all values of ship objects'''

        self.player1.hp = self.player1.max_hp
        self.player1.bullets_active = 0
        self.player1.turning = False
        self.player1.center_ship()

        self.player2.hp = self.player2.max_hp
        self.player2.bullets_active = 0
        self.player2.turning = False
        self.player2.center_ship()
        
        self.bullets.empty()
        self.winner=None
        self.game_active=True


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.background, (0,0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.player1.blitme()
        self.player2.blitme()
        self.aliens.draw(self.screen)
        self._draw_health_bars()

        if self.winner is not None:
            self._draw_winner()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
