'''
Tank sprites found on itch.io by author jh2assets https://jimhatama.itch.io/
'''
import arcade
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Potential Game #1"

HULL_TRAVERSE = .5
TURRET_TRAVERSE = .25

class Environment():
    def __init__(self):
        self.background_color = arcade.set_background_color(arcade.color.ARMY_GREEN)


    def draw(self):
        pass

class Tank():
    def __init__(self, hull_img, turret_img):
        
        self.max_speed = 0
        self.max_reverse_speed = 0
        self.acceleration = 0
        self.speed = 0
        self.is_moving = False
        # Hull
        self.hull_center_x = 0
        self.hull_center_y = 0
        self.hull_angle = 0
        self.hull_img = hull_img
        self.hull_texture = arcade.load_texture(self.hull_img)
        # Turret
        self.turret_center_x = self.hull_center_x
        self.turret_center_y = self.hull_center_y
        self.turret_angle = 0
        self.turret_img = turret_img
        self.turret_texture = arcade.load_texture(self.turret_img)

    def draw(self):
        arcade.draw_texture_rectangle(self.hull_center_x, self.hull_center_y, self.hull_texture.width, self.hull_texture.height, self.hull_texture, self.hull_angle, 255)
        arcade.draw_texture_rectangle(self.hull_center_x, self.hull_center_y, self.turret_texture.width, self.turret_texture.height, self.turret_texture, self.turret_angle, 255)

    def is_off_screen(self, screen_width, screen_height):
        if self.hull_center_x + (self.hull_texture.width / 8) >= screen_width: # x increases "right" ->
            self.hull_center_x = screen_width - (self.hull_texture.width / 8) 
        
        if self.hull_center_y + (self.hull_texture.height / 4) >= screen_height: # y increases "up"
            self.hull_center_y = screen_height - (self.hull_texture.height / 4) 
            
        if self.hull_center_x - (self.hull_texture.width / 2) <= 0: # x decreases "left"
            self.hull_center_x = 0 + (self.hull_texture.width / 6)
        
        if self.hull_center_y - (self.hull_texture.height / 4) <= 0 or self.hull_center_y + (self.hull_texture.height / 4) <= 0: # y decreases "down"
            self.hull_center_y = 0 + (self.hull_texture.height / 4)

    def left(self): # Change angle
        self.hull_angle += HULL_TRAVERSE
    
    def right(self):
        self.hull_angle -= HULL_TRAVERSE

    def forward(self):
        self.is_moving = True
        self.hull_center_x += math.cos(math.radians(self.hull_angle + 90)) * (self.speed)
        self.hull_center_y += math.sin(math.radians(self.hull_angle + 90)) * (self.speed)
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        elif self.speed >= self.max_speed:
            self.speed = self.max_speed
            
    def reverse(self):
        self.is_moving = True
        self.hull_center_x -= math.cos(math.radians(self.hull_angle + 90)) * (-self.speed)
        self.hull_center_y -= math.sin(math.radians(self.hull_angle + 90)) * (-self.speed)
        if self.speed > self.max_reverse_speed:
            self.speed -= self.acceleration
        elif self.speed <= self.max_reverse_speed:
            self.speed = self.max_reverse_speed
    
    def deceleration(self):
        if self.is_moving == False:
            if self.speed > 0:
                self.hull_center_x += math.cos(math.radians(self.hull_angle + 90)) * (self.speed)
                self.hull_center_y += math.sin(math.radians(self.hull_angle + 90)) * (self.speed)
                self.speed -= (self.acceleration * 5)
            if self.speed < 0:
                self.hull_center_x -= math.cos(math.radians(self.hull_angle + 90)) * (-self.speed)
                self.hull_center_y -= math.sin(math.radians(self.hull_angle + 90)) * (-self.speed)
                self.speed += (self.acceleration * 5)
            elif self.speed == 0:
                self.speed = 0

class Player(Tank):
    def __init__(self):
        super().__init__("ww2_tanks_top_export\Tiger\ww2_top_view_hull3.png", "ww2_tanks_top_export\Tiger\ww2_top_view_turret3.png")
        self.max_speed = 0.75
        self.max_reverse_speed = -0.25
        self.acceleration = 0.005
        # Hull
        self.hull_center_x = SCREEN_WIDTH / 2
        self.hull_center_y = 50



 
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Initilize objects
        self.env = Environment()
        self.player = Player()
        self.key_list = set()

        # Implement Objects
        self.env.background_color

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
    def on_update(self, delta_time: float):
        self.check_keys()
        self.player.deceleration()
        self.player.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def check_keys(self):
        if arcade.key.LEFT in self.key_list or arcade.key.A in self.key_list:
            self.player.left()
        if arcade.key.RIGHT in self.key_list or arcade.key.D in self.key_list:
            self.player.right()
        if arcade.key.UP in self.key_list or arcade.key.W in self.key_list:
            self.player.forward()
        if arcade.key.DOWN in self.key_list or arcade.key.S in self.key_list:
            self.player.reverse()

    def on_key_press(self, key, modifiers):
        self.key_list.add(key)

    def on_key_release(self, key, modifiers):
        self.key_list.remove(key)
        self.player.is_moving = False



if __name__ == "__main__":
    app = Game()
    arcade.run()