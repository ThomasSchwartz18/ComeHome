import arcade
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_RED
from utils import draw_parallax_background

class GameOver(arcade.View):
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score

        # Background layers
        self.background_layers = []
        self.background_speeds = [0.05, 0.125, 0.25, 0.5]  # Parallax speeds
        self.background_offsets = [0, 0, 0, 0]  # Track each layer's horizontal offset

        # Load the GameOver image
        self.game_over_image = arcade.load_texture("assets/GameOver.png")
        
        self.total_coins_collected = 0
        
        # Coin animation
        self.coin_textures = []
        self.coin_frame_index = 0
        self.coin_frame_time = 0
        self.coin_frame_duration = 0.1  # Seconds per frame

        # Load the coin animation frames
        self.load_coin_animation()

    def load_coin_animation(self):
        """Load the coin animation frames."""
        sprite_sheet_path = "assets/coin.png"  # Path to the coin sprite sheet
        frame_width = 32  # Width of each frame
        frame_height = 32  # Height of each frame
        frame_count = 5  # Total number of frames in the sprite sheet

        for i in range(frame_count):
            x_frame = i * frame_width
            texture = arcade.load_texture(
                sprite_sheet_path,
                x=x_frame,
                y=0,
                width=frame_width,
                height=frame_height
            )
            self.coin_textures.append(texture)

    def on_show(self):
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.save_score()

        # Load background layers
        for i in range(1, 5):  # Load Background1.png to Background4.png
            layer = arcade.load_texture(f"assets/background/Background{i}.png")
            self.background_layers.append(layer)

        # Load total coins collected
        try:
            with open("game_watcher/total_coins.txt", "r") as file:
                self.total_coins_collected = int(file.read().strip())
        except FileNotFoundError:
            self.total_coins_collected = 0

    def save_score(self):
        """Save the player's score to a file."""
        if not os.path.exists("scores.txt"):
            with open("scores.txt", "w") as file:
                file.write(f"{self.final_score}\n")
        else:
            with open("scores.txt", "a") as file:
                file.write(f"{self.final_score}\n")

    def on_draw(self):
        """Render the Game Over screen."""
        self.clear()

        # Draw the Background Layers from the utils.py file
        draw_parallax_background(
                self.background_layers,
                self.background_offsets,
                self.background_speeds,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
            )
        
        # Draw the Game Over image scaled to the window size
        arcade.draw_lrwh_rectangle_textured(
            0,  # X-coordinate (top-left corner of the window)
            0,  # Y-coordinate (top-left corner of the window)
            SCREEN_WIDTH,  # Width of the window
            SCREEN_HEIGHT,  # Height of the window
            self.game_over_image
        )

        # Display final score
        rounded_final_score = round(self.final_score)
        arcade.draw_text(f"Final Score: {rounded_final_score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 250,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        
        # Draw total coins collected with animated coin
        coin_x = SCREEN_WIDTH / 15
        coin_y = SCREEN_HEIGHT - 45
        arcade.draw_texture_rectangle(
            coin_x - 20, coin_y + 13, 32, 32, self.coin_textures[self.coin_frame_index]
        )
        arcade.draw_text(f"{self.total_coins_collected}", coin_x, coin_y,
                        arcade.color.RED_ORANGE, font_size=25, anchor_x="left")

        # Display restart instructions
        arcade.draw_text("Press ENTER to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_update(self, delta_time):
        """Update the background scrolling and coin animation."""
        for i in range(len(self.background_layers)):
            self.background_offsets[i] += self.background_speeds[i]
        
        # Update coin animation
        self.coin_frame_time += delta_time
        if self.coin_frame_time > self.coin_frame_duration:
            self.coin_frame_time = 0
            self.coin_frame_index = (self.coin_frame_index + 1) % len(self.coin_textures)

    def on_key_press(self, key, modifiers):
        """Handle key press for restarting the game."""
        if key == arcade.key.ENTER:
            from menus.title import Title
            title_view = Title()
            self.window.show_view(title_view)
