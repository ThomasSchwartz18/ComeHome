import arcade
import math

class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Animation textures
        self.textures = []
        sprite_sheet_path = "assets/coin.png"  # Sprite sheet for the coin
        frame_width = 32
        frame_height = 32
        frame_count = 5  # Assuming 5 frames in the coin sprite sheet

        # Load frames from the sprite sheet
        for i in range(frame_count):
            x_frame = i * frame_width
            texture = arcade.load_texture(
                sprite_sheet_path,
                x=x_frame,
                y=0,
                width=frame_width,
                height=frame_height
            )
            self.textures.append(texture)

        # Set the first texture
        self.texture = self.textures[0]
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.frame_duration = 0.1  # Seconds per frame

        # Set position and movement
        self.center_x = x
        self.center_y = y
        self.change_x = -5  # Move left
        self.gravitating = False  # Whether the coin is gravitating towards the player
        self.scale = 1.0  # Initial scale

    def update_animation(self, delta_time):
        """Update the coin animation."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]

    def update(self, delta_time, player):
        """Move the coin and gravitate towards the player if close enough."""
        # Move normally to the left
        if not self.gravitating:
            self.center_x += self.change_x

        # Check distance to the player
        distance_to_player = math.sqrt((self.center_x - player.center_x) ** 2 + (self.center_y - player.center_y) ** 2)
        if distance_to_player < 100:  # Adjust the distance threshold as needed
            self.gravitating = True

        # If gravitating, move towards the player and shrink
        if self.gravitating:
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y
            angle = math.atan2(dy, dx)
            self.center_x += math.cos(angle) * 7  # Adjust speed towards player
            self.center_y += math.sin(angle) * 2
            self.scale = max(0.5, self.scale - 0.05)  # Shrink the coin, but don't shrink below 0.5
