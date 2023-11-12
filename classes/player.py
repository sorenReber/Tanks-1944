import arcade
import math
from .tank_base import Tank

class Player(Tank):
    def __init__(self, screen_x):
        super().__init__("ww2_tanks_top_export\Sherman\ww2_top_view_hull10.png",
                        "ww2_tanks_top_export\Sherman\ww2_top_view_turret10.png")
        self.max_speed = .75
        self.max_reverse_speed = -0.25
        self.acceleration = 0.0025
        self.hit_points = 100
        self.reload_speed = 180
        self.reload_timer = 0
        self.reloading = False
        # Hull
        self.hull_sprite.center_x = screen_x / 2
        self.hull_sprite.center_y = 50

        # Turret
        self.target_angle = 0
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y
        
    def reload(self):
        if self.reloading:
            self.reload_timer += 1
        if self.reload_timer == self.reload_speed:
            self.reloading = False
            self.reload_timer = 0

    def aim_at_point(self, mouse_x, mouse_y):
        x_diff = mouse_x - self.hull_sprite.center_x
        y_diff = mouse_y - self.hull_sprite.center_y
        target_angle = math.atan2(y_diff, x_diff)
        return target_angle
