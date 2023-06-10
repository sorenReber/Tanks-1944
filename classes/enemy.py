import arcade
import math
from classes.tank_base import Tank

# Attempt at AI enemy - Motionless at first!
class Enemy(Tank):
    def __init__(self):
        super().__init__("ww2_tanks_top_export\Tiger\ww2_top_view_hull3.png",
                        "ww2_tanks_top_export\Tiger\ww2_top_view_turret3.png")
        self.max_speed = .35
        #self.max_reverse_speed = -0.25
        self.acceleration = 0.005
        self.hit_points = 100
        self.reload_speed = 180
        self.reload_timer = 0
        self.reloading = False
        # Hull
        self.hull_sprite.center_x = 0
        self.hull_sprite.center_y = 0
        self.hull_sprite.angle = 180
        # Turret
        self.target_angle = 0
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y
        self.turret_sprite.angle = 180
        # AI? Bot behavior?
        self.spawned_in = False

    def aim_at_player(self, target_x, target_y):
        x_diff = target_x - self.hull_sprite.center_x
        y_diff = target_y - self.hull_sprite.center_y
        target_angle = math.atan2(y_diff, x_diff)
        return target_angle
    
    def take_damage(self, damage_amount):
        self.hit_points -= damage_amount
        return self.hit_points
    
    def rotate_hull(self, target_angle_radians):
        '''
        This function rotates the hull, but most importantly, it will tell the enemy to
        switch the direction it is rotating to the most optimum direction.
        Repurposed the turret traverse function to apply to the hull of the tank.
        '''
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi
        current_angle_radians = math.radians(self.hull_sprite.angle + 90)
        rot_speed_radians = math.radians(self.hull_traverse)
        # Angle difference between mouse position and current turret angle.
        angle_diff_radians = target_angle_radians - current_angle_radians
        # Figure out if we rotate clockwise or counter-clockwise based off the difference.
        if abs(angle_diff_radians) <= rot_speed_radians:
            current_angle_radians = target_angle_radians
            clockwise = None
        elif angle_diff_radians > 0 and abs(angle_diff_radians) < math.pi:
            clockwise = False
        elif angle_diff_radians > 0 and abs(angle_diff_radians) >= math.pi:
            clockwise = True
        elif angle_diff_radians < 0 and abs(angle_diff_radians) < math.pi:
            clockwise = True
        else:
            clockwise = False
        # Rotate the proper direction if needed
        if current_angle_radians != target_angle_radians and clockwise:
            current_angle_radians -= rot_speed_radians
        elif current_angle_radians != target_angle_radians:
            current_angle_radians += rot_speed_radians
        # Keep in a range of 0 to 2pi
        if current_angle_radians > 2 * math.pi:
            current_angle_radians -= 2 * math.pi
        elif current_angle_radians < 0:
            current_angle_radians += 2 * math.pi
        # Convert back to degrees
        self.hull_sprite.angle = math.degrees(current_angle_radians) - 90
