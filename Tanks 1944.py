'''
By Soren Reber
Tank sprites found on itch.io by author jh2assets https://jimhatama.itch.io/
Rock and bullet sprites is free from Kenny.nl https://kenney.nl/
Tank Cannon sound is from Freesound and is by GaryQ https://freesound.org/s/127845/
'''
import arcade
from Settings import *
from main_logic import *

# Constants


if __name__ == "__main__":
    app = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()