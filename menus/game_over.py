import arcade
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOver(arcade.View):
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.save_score()

    def save_score(self):
        """Save the player's score to a file."""
        if not os.path.exists("scores.txt"):
            with open("scores.txt", "w") as file:
                file.write(f"{self.final_score}\n")
        else:
            with open("scores.txt", "a") as file:
                file.write(f"{self.final_score}\n")

    def on_draw(self):
        self.clear()
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.RED, font_size=50, anchor_x="center")
        arcade.draw_text(f"Final Score: {self.final_score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Press ENTER to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from menus.title import Title
            title_view = Title()
            self.window.show_view(title_view)
