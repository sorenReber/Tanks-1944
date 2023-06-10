# By Soren Reber
'''
Tank sprites found on itch.io by author jh2assets https://jimhatama.itch.io/
Rock and bullet sprites is free from Kenny.nl https://kenney.nl/
Tank Cannon sound is from Freesound and is by GaryQ https://freesound.org/s/127845/
'''
import random
import arcade
import math

# Constants
SCREEN = arcade.get_display_size()
SCREEN_WIDTH = SCREEN[0]
SCREEN_HEIGHT = SCREEN[1]
SCREEN_TITLE = "Tanks 1944"

class Environment():
    def __init__(self, img):
        self.img = img
        self.sprite = arcade.Sprite(img, .5)
  
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
        self.hull_sprite.center_x = 0
        self.hull_sprite.center_y = 0
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
        self.sound = arcade.load_sound("tank-fire.wav")

    def check_collisions(self, list_1, list_2):
        hit = arcade.check_for_collision_with_lists(self.sprite, [list_1, list_2], 2)
        return hit

class Enemy_bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.damage = 25

class Player(Tank):
    def __init__(self):
        super().__init__("ww2_tanks_top_export\Tiger\ww2_top_view_hull3.png",
                        "ww2_tanks_top_export\Tiger\ww2_top_view_turret3.png")
        self.max_speed = .75
        self.max_reverse_speed = -0.25
        self.acceleration = 0.005
        self.hit_points = 100
        self.reload_speed = 180
        self.reload_timer = 0
        self.reloading = False
        # Hull
        self.hull_sprite.center_x = SCREEN_WIDTH / 2
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
        self.hull_sprite.center_x = SCREEN_WIDTH / 2
        self.hull_sprite.center_y = 850
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
        The arcade website has excellent examples and I used example code for rotating a 
        tank.
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

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
        arcade.Window.maximize(self)
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        # Initialize player
        self.player = Player()
        # Start Music
        bg_music = arcade.load_sound(":resources:music/1918.mp3", True)
        arcade.play_sound(bg_music, looping= True)
        # Lists
        self.player_bullets = []
        self.enemies_list = []
        self.key_list = set()
        self.tree_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.player_bullet_sprites = arcade.SpriteList()
        #self.enemies_sprites = arcade.SpriteList()
        

    def setup(self):
        # Create a random number of trees and add to the tree_list.
        for _ in range(random.randint(5, 15)):
            tree = Tree()
            tree.sprite.center_x = random.randint(35, SCREEN_WIDTH - 35)
            tree.sprite.center_y = random.randint(50, SCREEN_HEIGHT - 35)
            self.tree_list.append(tree.sprite)
        # Create a random number of rocks and add to the rock_list.
        for _ in range(random.randint(8, 20)):
            rock = Rock()
            rock.sprite.center_x = random.randint(35, SCREEN_WIDTH - 35)
            rock.sprite.center_y = random.randint(50, SCREEN_HEIGHT - 35)
            rock.sprite.angle = random.randrange(0, 180)
            self.rock_list.append(rock.sprite)
        for _ in range(random.randint(3, 8)):
            enemy = Enemy()
            enemy.hull_sprite.center_x = random.randint(50, SCREEN_WIDTH - 50)
            enemy.hull_sprite.center_y = random.randint(450, SCREEN_HEIGHT - 50)
            self.enemies_list.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.player_bullet_sprites.draw()
        self.player.on_draw()
        self.tree_list.draw()
        self.rock_list.draw()
        for enemy in self.enemies_list:
            if enemy.hull_sprite.center_y < self.player.hull_sprite.center_y + 550: 
                enemy.spawned_in = True
            if enemy.spawned_in == True:
                enemy.on_draw()

    def on_update(self, delta_time: float):
        self.check_keys()
        self.player.deceleration()
        self.player.screen_edge(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player.rotate_turret(self.player.target_angle)
        self.player.reload()

        # Enemy targeting
        for enemy in self.enemies_list:
            if enemy.spawned_in == True:
                enemy.screen_edge(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemy.forward()
                player_target = enemy.aim_at_player(self.player.hull_sprite.center_x, self.player.hull_sprite.center_y)
                enemy.rotate_turret(player_target)
                enemy.rotate_hull(player_target)

        for bullet in self.player_bullets:
            bullet.update()
        # Check the bullets for collisions and if they are off screen.
        for bullet in self.player_bullet_sprites:
            bullet_hit_environment = arcade.check_for_collision_with_lists(bullet, [self.tree_list, self.rock_list,], 2)
            if len(bullet_hit_environment) > 0:
                bullet.remove_from_sprite_lists()
            if bullet.bottom > SCREEN_HEIGHT or bullet.left > SCREEN_WIDTH or bullet.bottom < 0 or bullet.left < 0:
                bullet.remove_from_sprite_lists()
            # Check trees for collision with bullets
            for tree in self.tree_list:
                if tree in bullet_hit_environment:
                    tree.remove_from_sprite_lists()
            
            for enemy in self.enemies_list:
                if enemy.spawned_in == True:
                    bullet_hit_enemy = arcade.check_for_collision(bullet, enemy.hull_sprite)
                    for bullet_obj in self.player_bullets:
                        if bullet_hit_enemy:
                            enemy.take_damage(bullet_obj.damage)
                            bullet.remove_from_sprite_lists()
                            self.player_bullets.remove(bullet_obj)
                            if enemy.hit_points <= 0:
                                self.enemies_list.remove(enemy)
        
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
        # Creates a bullet sprite and object. Append the sprite to a sprite list and the object to an object list.
        if self.player.reloading == False:
            player_bullet = Player_bullet()
            player_bullet.sprite.angle = self.player.turret_sprite.angle
            player_bullet.sprite.center_x = self.player.turret_sprite.center_x
            player_bullet.sprite.center_y = self.player.turret_sprite.center_y
            # Play the tank cannon sound
            arcade.play_sound(player_bullet.sound)
            self.player_bullets.append(player_bullet)
            self.player_bullet_sprites.append(player_bullet.sprite)
            # Sets the reload to true so there is time between shots.
            self.player.reloading = True
            self.player.reload_timer = 0
        

if __name__ == "__main__":
    app = Game()
    app.setup()
    arcade.run()