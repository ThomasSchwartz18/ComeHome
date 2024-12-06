import arcade
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Pause(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Reference to the main game view

    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Game Paused", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Press ESC to Resume", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)  # Resume the game
