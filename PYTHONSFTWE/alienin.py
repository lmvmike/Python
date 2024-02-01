#from concurrent.futures.process import _ThreadWakeup
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #overall class to manage game assets and behavoir
    def __init__(self):
        #initalize the game and create game recourses

        pygame.init()
        self.settings = Settings()

        #tell pygame to determine the size of the screen, set screen width and height
        self.screen = pygame.display.setmode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Lam Tran Alien Invasion")

        #create an instance to store game settingd
        self.stats = GameStats(self)

        #set the BG color
        self.bg_color = (200,230,230)

        self.ship =Ship(self)
        self.bullets = pygame.sprite.Group()

        #add in the alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        #Start the main loop

        while True:
            #call to check to see if any keyboard events have occured
            self._check_events()
            #check to see if the game is still alive (more ship left)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        #reponse to keypress and mouse events
            #did the player quit the game?
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                sys.exit()
            #did the player press the right or left arrow key?
            elif event.type ==pygame.KEYDOWN:
                self._check_keydown_events(event)
            #did the player stop holding down the arrow key?
            elif event.type ==pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        #is the key the right arrow or is it the left arrow
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = True
        #did the player hit the Q key to quit the game?
        elif event.key ==pygame.K_q:
            sys.exit()
        #did the player hit theh space bar to shoot bullets?
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        # Did the player stop holding down the arrow keys?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        #Limited the number of bullets a player can have at a time by adding aconstant to the settings file
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #update positions of the bullets and get rid of old bullets.
        self.bullets.update()

    #get rid of bullets that have disappeared off the screen because they are still there in the game and take up memory and execution time
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
                # determine how many bullets stil exist in the game to veridy they are being deleted
                #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #respond to bullet_alien collisions
        #check for any bullets that have hit aliens if so get rid of the bullet and alien
        collisions =pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        #check to see if the aliens group is empty and if so, create a new fleet
        if not self.aliens:
            #destroy any exisitng ullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        #update the position of all aliens in the fleet
        #check if the fleet is at an edge then update the position of all aliens in the flee
        self._check_fleet_egdes()
        self.aliens.update()

        #look for alien_ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("SHIP HIT!!!")
            self._ship_hit()#look for aliens hitting the botton of the screen
            self._check_aliens_bottom()

#Add a method to create a fleet of aliens
    def _create_fleet(self):
        """create the fleet of aliens"""
        #make a single alien.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size 
        #determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #determine the number of rows of alinens that fit on the scrren
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range (number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        alien_width = aliens.rect.width
        aliens.x = alien_width + 2 * alien_width * alien_number
        aliens.rect.x = aliens.x
        aliens.x = alien_width + 2* alien_width * alien_width * alien_number
        self.aliens.add(aliens)

    def _check_fleet_edges(self):
        #respond approriately if any alines have reached an egde
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #drop the entiner fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #respond to the ship being hit by an alien
        if self.stats.ships_left>0:
            #decrement the number of ships left
            self.stats.ship_left -= 1

            #get rid of any remaining alines and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and cneter the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause for half a second
            sleep (0.5)
        else:
            self.stats.games_active = False

    def _check_aliens_botton(self):
        #check if any aliens have reached the botton of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.botton >= screen_rect.bottom:
                #treat tthis the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        #update images onn the screen and flip to new screen
        #redrae the screen each pass through th eloop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        #draw bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw the alien
            self.aliens.draw(self.screen)

        #make the most recentlhy drawn screen visible
        pygame.display.flip()
        
if __name__ =='main__':
    #make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

quit()