import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Title(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_layers = []
        self.background_speeds = [0.05, 0.125, 0.25, 0.5]  # Parallax speeds
        self.background_offsets = [0, 0, 0, 0]  # Track each layer's horizontal offset

        # Button properties
        self.button_center_x = SCREEN_WIDTH / 2
        self.button_center_y = SCREEN_HEIGHT / 2 - 250
        self.button_width = 200
        self.button_height = 50

        self.leaderboard = []

        # Load the title image
        self.title_image = arcade.load_texture("assets/TitleMenu-title.png")
        
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
        self.load_leaderboard()

        # Load background layers
        for i in range(1, 5):  # Load Background1.png to Background4.png
            layer = arcade.load_texture(f"assets/background/Background{i}.png")
            self.background_layers.append(layer)
            
        # Add the title image as the topmost background layer
        title_layer = arcade.load_texture("assets/TitleMenu-title.png")
        self.background_layers.append(title_layer)
        self.background_speeds.append(0)  # No movement for the title image
        self.background_offsets.append(0)  # Static offset
        
        # Load total coins collected
        try:
            with open("game_watcher/total_coins.txt", "r") as file:
                self.total_coins_collected = int(file.read().strip())
        except FileNotFoundError:
            self.total_coins_collected = 0
            

    def load_leaderboard(self):
        """Load the top 5 scores from a file."""
        import os
        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as file:
                scores = file.readlines()
            self.leaderboard = sorted([int(score.strip()) for score in scores], reverse=True)[:3]
        else:
            self.leaderboard = []

    def on_draw(self):
        """Render the title screen."""
        self.clear()

        # Draw background layers
        for i, layer in enumerate(self.background_layers):
            offset = self.background_offsets[i] % SCREEN_WIDTH
            arcade.draw_lrwh_rectangle_textured(-offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT, layer)
            arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH - offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT, layer)

        # Draw the title image scaled to the window size
        arcade.draw_lrwh_rectangle_textured(
            0,  # X-coordinate (top-left corner of the window)
            0,  # Y-coordinate (top-left corner of the window)
            SCREEN_WIDTH,  # Width of the window
            SCREEN_HEIGHT,  # Height of the window
            self.title_image
        )

        # Draw Start Button
        arcade.draw_rectangle_filled(self.button_center_x, self.button_center_y,
                                    self.button_width, self.button_height, arcade.color.GREEN)
        arcade.draw_text("START", self.button_center_x, self.button_center_y,
                        arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

        # Draw leaderboard
        arcade.draw_text("High Scores:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 250,
                        arcade.color.LIGHT_GREEN, font_size=35, anchor_x="center")
        for i, score in enumerate(self.leaderboard):
            arcade.draw_text(f"{i + 1}....{score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 190 - i * 30,
                            arcade.color.LIGHT_GREEN, font_size=20, anchor_x="center")
            
        # Draw total coins collected with animated coin
        coin_x = SCREEN_WIDTH / 15
        coin_y = SCREEN_HEIGHT - 45
        arcade.draw_texture_rectangle(
            coin_x - 20, coin_y + 13, 32, 32, self.coin_textures[self.coin_frame_index]
        )
        arcade.draw_text(f"{self.total_coins_collected}", coin_x, coin_y,
                        arcade.color.LIGHT_GREEN, font_size=25, anchor_x="left")

    def on_update(self, delta_time):
        """Update the background scrolling."""
        for i in range(len(self.background_layers)):
            self.background_offsets[i] += self.background_speeds[i]
        
        # Update coin animation
        self.coin_frame_time += delta_time
        if self.coin_frame_time > self.coin_frame_duration:
            self.coin_frame_time = 0
            self.coin_frame_index = (self.coin_frame_index + 1) % len(self.coin_textures)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse click for the start button."""
        if self.button_center_x - self.button_width / 2 < x < self.button_center_x + self.button_width / 2 and \
           self.button_center_y - self.button_height / 2 < y < self.button_center_y + self.button_width / 2:
            from game_window import GameWindow
            game_view = GameWindow()
            game_view.setup()
            self.window.show_view(game_view)
