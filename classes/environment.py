import arcade
class Environment():
    def __init__(self, img):
        self.img = img
        self.sprite = arcade.Sprite(img, .5)
class Tree(Environment):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/treeGreen_large.png")

class Rock(Environment):
    def __init__(self):
        super().__init__('Tanks 1944/environment_png/rock_2.png')
