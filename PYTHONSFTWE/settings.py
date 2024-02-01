import pygame 
class Settings:
    """ A class to store all settings for Alien Invasion"""

    def __init__(self):
        """ Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1500
        self.screen_height = 1400
        self.bg_color = (245, 245, 245)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        """ Bullet settings - dark grey bullets that a re 3 pixels wide and 15
        pixels high. Bullets travel slower than the ship."""
        self.bullet_speed = 1.5
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 0, 0)          # 60, 60, 60
        self.bullets_allowed = 1
        # alien settings
        self.alien_speed = 15 
        self.fleet_drop_speed = 5
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settign thay chenge trhought the game  """
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

        #fleed_direction of 1 represents right and -1 represent left

        self.fleet_direction = 1

        #scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
