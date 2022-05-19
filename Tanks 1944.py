'''
Tank sprites found on itch.io by author jh2assets https://jimhatama.itch.io/
'''
import random
import arcade
import math

from numpy import angle

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Tanks 1944"


class Environment():
    def __init__(self, img):
        self.img = img
        self.sprite = arcade.Sprite(img, .5)

class Bush(Environment):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/treeGreen_small.png")

  
class Tree(Environment):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/treeGreen_large.png")

class Rock(Environment):
    def __init__(self):
        super().__init__('environment_png/rock_2.png')


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
        self.hull_sprite.center_x = 50
        self.hull_sprite.center_y = 50
        self.hull_sprite.angle = 0
        self.hull_traverse = 0.5

        # Turret
        self.turret_sprite = arcade.Sprite(turret_img, 1)
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y
        self.turret_sprite.angle = 0
        self.turret_traverse = 0.25

    def on_draw(self):
        self.hull_sprite.draw()
        self.turret_sprite.draw()
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y

    def screen_edge(self, screen_width, screen_height):
        if self.hull_sprite.center_x + (self.hull_sprite.width / 5) >= screen_width: # x increases "right" ->
            self.hull_sprite.center_x = screen_width - (self.hull_sprite.width / 5) 
        
        if self.hull_sprite.center_y + (self.hull_sprite.height / 5) >= screen_height: # y increases "up"
            self.hull_sprite.center_y = screen_height - (self.hull_sprite.height / 5) 
            
        if self.hull_sprite.center_x - (self.hull_sprite.width / 5) <= 0: # x decreases "left"
            self.hull_sprite.center_x = 0 + (self.hull_sprite.width / 5)
        
        if self.hull_sprite.center_y - (self.hull_sprite.height / 5) <= 0 :# y decreases "down"
            self.hull_sprite.center_y = 0 + (self.hull_sprite.height / 5)

    def left(self): # Change angle
        self.hull_sprite.angle += self.hull_traverse
    
    def right(self):
        self.hull_sprite.angle -= self.hull_traverse

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
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi
        current_angle_radians = math.radians(self.turret_sprite.angle + 90)
        rot_speed_radians = math.radians(self.turret_traverse)
        # What is the difference between what we want, and where we are?
        angle_diff_radians = target_angle_radians - current_angle_radians
        # Figure out if we rotate clockwise or counter-clockwise
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

class Bullet():
    def __init__(self):
        self.damage = 0
        self.bullet_speed = 5
        self.sprite = arcade.Sprite("bullet.png", .25, flipped_vertically=True)
        self.sprite.angle = 0
    
    def update(self):
        self.sprite.center_x += math.cos(math.radians(self.sprite.angle + 90)) * (self.bullet_speed)
        self.sprite.center_y += math.sin(math.radians(self.sprite.angle + 90)) * (self.bullet_speed)

class Player_bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.bullet_speed = 5.5
    def check_collisions(self, list_1, list_2):
        hit = arcade.check_for_collision_with_lists(self.sprite, [list_1, list_2], 2)
        return hit

class Enemy_bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.damage = 25

class Player(Tank):
    def __init__(self):
        super().__init__("ww2_tanks_top_export\Tiger\ww2_top_view_hull3.png", "ww2_tanks_top_export\Tiger\ww2_top_view_turret3.png")
        self.max_speed = .75
        self.max_reverse_speed = -0.25
        self.acceleration = 0.005
        self.hit_points = 100
        
        # Hull
        self.hull_sprite.center_x = SCREEN_WIDTH / 2
        self.hull_sprite.center_y = 50
        self.target_angle = 0
        self.turret_sprite.center_x = self.hull_sprite.center_x
        self.turret_sprite.center_y = self.hull_sprite.center_y

    def aim_at_point(self, mouse_x, mouse_y):
        x_diff = mouse_x - self.hull_sprite.center_x
        y_diff = mouse_y - self.hull_sprite.center_y
        target_angle = math.atan2(y_diff, x_diff)
        return target_angle

 
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        # Initialize player
        self.player = Player()
        
        # Lists
        self.player_bullets = []
        self.enemies_list = []
        self.key_list = set()
        self.tree_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.player_bullet_sprites = arcade.SpriteList()

    def setup(self):
        # Create a random number of trees and add to the tree_list.
        for i in range(random.randint(5, 15)):
            tree = Tree()
            tree.sprite.center_x = random.randint(35, SCREEN_WIDTH - 35)
            tree.sprite.center_y = random.randint(35, SCREEN_HEIGHT - 35)
            self.tree_list.append(tree.sprite)
        # Create a random number of rocks and add to the rock_list.
        for i in range(random.randint(8, 20)):
            rock = Rock()
            rock.sprite.center_x = random.randint(35, SCREEN_WIDTH - 35)
            rock.sprite.center_y = random.randint(35, SCREEN_HEIGHT - 35)
            rock.sprite.angle = random.randrange(0, 180)
            self.rock_list.append(rock.sprite)

    def on_draw(self):
        arcade.start_render()
        self.player_bullet_sprites.draw()
        self.player.on_draw()
        self.tree_list.draw()
        self.rock_list.draw()


    def on_update(self, delta_time: float):
        self.check_keys()
        self.player.deceleration()
        self.player.screen_edge(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player.rotate_turret(self.player.target_angle)
        for bullet in self.player_bullets:
            bullet.update()
        
        for bullet in self.player_bullet_sprites:
            hit = arcade.check_for_collision_with_lists(bullet, [self.tree_list, self.rock_list], 2)
            if len(hit) > 0:
                bullet.remove_from_sprite_lists()
        
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
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.player.target_angle = self.player.aim_at_point(x, y)

    def on_mouse_press(self, x, y, button, modifier):
        player_bullet = Player_bullet()
        player_bullet.sprite.angle = self.player.turret_sprite.angle
        player_bullet.sprite.center_x = self.player.turret_sprite.center_x
        player_bullet.sprite.center_y = self.player.turret_sprite.center_y
        self.player_bullets.append(player_bullet)
        self.player_bullet_sprites.append(player_bullet.sprite)
        

if __name__ == "__main__":
    app = Game()
    app.setup()
    arcade.run()