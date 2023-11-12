import arcade
import random
from classes.environment import *
from classes.bullet import *
from classes.player import *
from classes.enemy import *

'''Main Game class and logic'''

class Game(arcade.Window):
    def __init__(self, screen_x, screen_y, title):
        self.widthx = screen_x
        self.heighty = screen_y
        super().__init__(self.widthx, self.heighty, title, center_window=True)
        arcade.Window.maximize(self)
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        # Initialize player
        self.player = Player(self.widthx)
        # Start Music
        bg_music = arcade.load_sound(":resources:music/1918.mp3", True)
        arcade.play_sound(bg_music, looping= True)
        # Lists
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies_list = []
        self.key_list = set()
        self.tree_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.player_bullet_sprites = arcade.SpriteList()
        self.enemy_bullet_sprites = arcade.SpriteList()

        
    def setup(self):
        # Create a random number of trees and add to the tree_list.
        for _ in range(random.randint(5, 15)):
            tree = Tree()
            tree.sprite.center_x = random.randint(35, self.widthx - 35)
            tree.sprite.center_y = random.randint(50, self.heighty - 35)
            self.tree_list.append(tree.sprite)

        # Create a random number of rocks and add to the rock_list.
        for _ in range(random.randint(8, 20)):
            rock = Rock()
            rock.sprite.center_x = random.randint(35, self.widthx - 35)
            rock.sprite.center_y = random.randint(50, self.heighty - 35)
            rock.sprite.angle = random.randrange(0, 180)
            self.rock_list.append(rock.sprite)

        # Create an initial number of enemies 
        for _ in range(random.randint(3, 5)):
            enemy = Enemy()
            enemy.hull_sprite.center_x = random.randint(10, self.widthx - 10)
            enemy.hull_sprite.center_y = random.randint(self.heighty + 10, self.heighty + 150)
            enemy.turret_sprite.center_x = enemy.hull_sprite.center_x
            enemy.turret_sprite.center_y = enemy.hull_sprite.center_y
            self.enemies_list.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.player_bullet_sprites.draw()
        self.enemy_bullet_sprites.draw()
        self.player.on_draw()
        self.tree_list.draw()
        self.rock_list.draw()
        for enemy in self.enemies_list:
            if enemy.hull_sprite.center_y < self.heighty + 150 : 
                enemy.spawned_in = True
            if enemy.spawned_in == True:
                enemy.on_draw()

    def on_update(self, delta_time: float):
        self.check_keys()
        self.player.deceleration()
        self.player.screen_edge(self.widthx, self.heighty)
        self.player.rotate_turret(self.player.target_angle)
        self.player.reload()

        # Enemy targeting
        for enemy in self.enemies_list:
            if enemy.spawned_in == True:
                enemy.forward()
                enemy.reload()
                player_target = enemy.aim_at_player(self.player.hull_sprite.center_x, self.player.hull_sprite.center_y)
                enemy.rotate_turret(player_target)
                enemy.rotate_hull(player_target)
                print(f"player target = {player_target}")
                print(enemy.turret_sprite.angle)
                #while player_target == 0:
                if enemy.reloading == False:
                    enemy_bullet = Enemy_bullet()
                    enemy_bullet.sprite.angle = enemy.turret_sprite.angle + (.25 * random.randint(-20, 20))
                    enemy_bullet.sprite.center_x = enemy.turret_sprite.center_x
                    enemy_bullet.sprite.center_y = enemy.turret_sprite.center_y
                    # Play the tank cannon sound
                    arcade.play_sound(enemy_bullet.sound)
                    self.enemy_bullets.append(enemy_bullet)
                    self.enemy_bullet_sprites.append(enemy_bullet.sprite)
                    # Sets the reload to true so there is time between shots.
                    enemy.reloading = True
                    enemy.reload_timer = 0

        # Update bullets
        for bullet in self.player_bullets:
            bullet.update()
            bullet_hit_environment = bullet.check_collisions(self.tree_list, self.rock_list)
            if bullet_hit_environment:
                self.player_bullets.remove(bullet)
            if bullet.center_y > self.heighty or bullet.center_x > self.widthx or bullet.center_x < 0 or bullet.center_y < 0:
                self.player_bullets.remove(bullet)
        for bullet in self.enemy_bullets:
            bullet.update()
            bullet_hit_environment = bullet.check_collisions(self.tree_list, self.rock_list)
            if bullet_hit_environment:
                self.enemy_bullets.remove(bullet)
            if bullet.center_y > self.heighty or bullet.center_x > self.widthx or bullet.center_x < 0 or bullet.center_y < 0:
                self.player_bullets.remove(bullet)

        # Check the bullets for collisions and if they are off screen.
        for bullet in self.player_bullet_sprites:
            bullet_hit_environment = arcade.check_for_collision_with_lists(bullet, [self.tree_list, self.rock_list,], 2)
            if len(bullet_hit_environment) > 0:
                bullet.remove_from_sprite_lists()
            if bullet.bottom > self.heighty or bullet.left > self.widthx or bullet.bottom < 0 or bullet.left < 0:
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
        for bullet in self.enemy_bullet_sprites:
            bullet_hit_environment = arcade.check_for_collision_with_lists(bullet, [self.tree_list, self.rock_list,], 2)
            if len(bullet_hit_environment) > 0:
                bullet.remove_from_sprite_lists()
            if bullet.bottom > self.heighty or bullet.left >self.widthx or bullet.bottom < 0 or bullet.left < 0:
                bullet.remove_from_sprite_lists()
            # Check trees for collision with bullets
            for tree in self.tree_list:
                if tree in bullet_hit_environment:
                    tree.remove_from_sprite_lists()

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
            player_bullet.sprite.angle = self.player.turret_sprite.angle + (.1*random.randint(-8, 8))
            player_bullet.sprite.center_x = self.player.turret_sprite.center_x
            player_bullet.sprite.center_y = self.player.turret_sprite.center_y
            # Play the tank cannon sound
            arcade.play_sound(player_bullet.sound)
            self.player_bullets.append(player_bullet)
            self.player_bullet_sprites.append(player_bullet.sprite)
            # Sets the reload to true so there is time between shots.
            self.player.reloading = True
            self.player.reload_timer = 0