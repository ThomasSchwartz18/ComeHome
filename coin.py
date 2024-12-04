import math
from utils import AnimatedSprite

class Coin(AnimatedSprite):
    def __init__(self, x, y):
        # Initialize the AnimatedSprite with the coin sprite sheet
        super().__init__(
            sprite_sheet_path="assets/coin.png",
            frame_width=32,
            frame_height=32,
            frame_count=5,
            scale=0.5,
            frame_duration=0.5  # Animation frame duration
        )

        # Set position and movement
        self.center_x = x
        self.center_y = y
        self.change_x = -5  # Move left
        self.gravitating = False  # Whether the coin is gravitating towards the player

    def update(self, delta_time, player):
        """Move the coin and gravitate towards the player if close enough."""
        # Update the animation
        self.update_animation(delta_time)

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
