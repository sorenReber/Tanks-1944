import arcade
import math

class Bullet():
    def __init__(self):
        self.damage = 0
        self.bullet_speed = 5
        self.sprite = arcade.Sprite("bullet.png", .25, flipped_vertically=True)
        self.sprite.angle = 0
        self.sound = arcade.load_sound("tank-fire.wav")
        self.center_x = self.sprite.center_x
        self.center_y = self.sprite.center_y
    
    def update(self):
        self.sprite.center_x += math.cos(math.radians(self.sprite.angle + 90)) * (self.bullet_speed)
        self.sprite.center_y += math.sin(math.radians(self.sprite.angle + 90)) * (self.bullet_speed)
    
    def check_collisions(self, list_1, list_2):
        hit = arcade.check_for_collision_with_lists(self.sprite, [list_1, list_2], 2)
        return hit

class Player_bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.bullet_speed = 5.5

class Enemy_bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.damage = 50