import arcade
import math

class Tank():
    def __init__(self, hull_img, turret_img):      
        self.max_speed = 0
        self.max_reverse_speed = 0
        self.acceleration = 0
        self.speed = 0
        self.is_moving = False
        self.hit_points = 0
 
        # Hull
        self.hull_sprite = arcade.Sprite(hull_img, 1)
        self.hull_sprite.center_x = 0
        self.hull_sprite.center_y = 0
        self.hull_sprite.angle = 0
        self.hull_traverse = 0.15

        # Turret
        self.turret_sprite = arcade.Sprite(turret_img, 1)
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y
        self.turret_sprite.angle = 0
        self.turret_traverse = 0.35

    def on_draw(self):
        self.hull_sprite.draw()
        self.turret_sprite.draw()
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y

    # Keep the sprite within the arcade window.
    def screen_edge(self, screen_width, screen_height):
        if self.hull_sprite.center_x + (self.hull_sprite.width / 5) >= screen_width: # x increases "right" ->
            self.hull_sprite.center_x = screen_width - (self.hull_sprite.width / 5) 
        
        if self.hull_sprite.center_y + (self.hull_sprite.height / 5) >= screen_height: # y increases "up"
            self.hull_sprite.center_y = screen_height - (self.hull_sprite.height / 5) 
            
        if self.hull_sprite.center_x - (self.hull_sprite.width / 5) <= 0: # x decreases "left"
            self.hull_sprite.center_x = 0 + (self.hull_sprite.width / 5)
        
        if self.hull_sprite.center_y - (self.hull_sprite.height / 5) <= 0 :# y decreases "down"
            self.hull_sprite.center_y = 0 + (self.hull_sprite.height / 5)
    # Change angle
    def left(self):
        self.hull_sprite.angle += self.hull_traverse
    
    def right(self):
        self.hull_sprite.angle -= self.hull_traverse
    # Forward, reverse, and deceleration
    def forward(self):
        self.is_moving = True
        self.hull_sprite.center_x += math.cos(math.radians(self.hull_sprite.angle + 90)) * (self.speed)
        self.hull_sprite.center_y += math.sin(math.radians(self.hull_sprite.angle + 90)) * (self.speed)
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        elif self.speed >= self.max_speed:
            self.speed = self.max_speed
            
    def reverse(self):
        self.is_moving = True
        self.hull_sprite.center_x -= math.cos(math.radians(self.hull_sprite.angle + 90)) * (-self.speed)
        self.hull_sprite.center_y -= math.sin(math.radians(self.hull_sprite.angle + 90)) * (-self.speed)
        if self.speed > self.max_reverse_speed:
            self.speed -= self.acceleration
        elif self.speed <= self.max_reverse_speed:
            self.speed = self.max_reverse_speed
    
    def deceleration(self):
        if self.is_moving == False:
            if self.speed > .1:
                self.hull_sprite.center_x += math.cos(math.radians(self.hull_sprite.angle + 90)) * (self.speed)
                self.hull_sprite.center_y += math.sin(math.radians(self.hull_sprite.angle + 90)) * (self.speed)
                self.speed -= (self.acceleration * 5)
            if self.speed < -.1:
                self.hull_sprite.center_x -= math.cos(math.radians(self.hull_sprite.angle + 90)) * (-self.speed)
                self.hull_sprite.center_y -= math.sin(math.radians(self.hull_sprite.angle + 90)) * (-self.speed)
                self.speed += (self.acceleration * 5)
            elif self.speed > -.1 and self.speed < .1:
                self.speed = 0

    def rotate_turret(self, target_angle_radians):
        '''
        This function rotates the turret, but most importantly, it will tell the turret to
        switch the direction it is rotating to the most optimum direction.
        The arcade website has excellent examples and I used example code for rotating a 
        tank and altered it to apply to the tank turret.
        '''
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi
        current_angle_radians = math.radians(self.turret_sprite.angle + 90)
        rot_speed_radians = math.radians(self.turret_traverse)
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
        self.turret_sprite.angle = math.degrees(current_angle_radians) - 90