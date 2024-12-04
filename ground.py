import arcade
import random
from constants import GROUND_HEIGHT, SCREEN_WIDTH
from utils import AnimatedSprite


class GroundTile(AnimatedSprite):
    """A single ground tile with animated sprite."""
    def __init__(self, x, y, sprite_sheet_path, frame_width, frame_height, frame_count, frame_duration):
        super().__init__(
            sprite_sheet_path=sprite_sheet_path,
            frame_width=frame_width,
            frame_height=frame_height,
            frame_count=frame_count,
            scale=0.1,  # No scaling applied
            frame_duration=frame_duration
        )
        self.center_x = x
        self.center_y = y

        # Randomize the starting frame to offset animations
        self.current_frame = random.randint(0, frame_count - 1)
        self.time_since_last_frame = random.uniform(0, frame_duration)


class Ground:
    def __init__(self):
        self.tiles = arcade.SpriteList()

        # Path to the ground tile sprite sheet
        sprite_sheet_path = "assets/tiles/GroundTile_Sprite.png"

        # Tile dimensions
        self.tile_width = 64
        self.tile_height = 100
        frame_width = 640  # Width of each frame in the sprite sheet
        frame_height = 1000  # Height of each frame in the sprite sheet
        frame_count = 5  # Number of animation frames in the sprite sheet
        frame_duration = 0.1  # Duration of each frame in seconds

        # Create and position tiles for an extra screen width
        for x in range(0, SCREEN_WIDTH * 2, self.tile_width):
            tile = GroundTile(
                x=x,
                y=GROUND_HEIGHT // 2,
                sprite_sheet_path=sprite_sheet_path,
                frame_width=frame_width,
                frame_height=frame_height,
                frame_count=frame_count,
                frame_duration=frame_duration,
            )
            self.tiles.append(tile)

    def update(self, delta_time, speed):
        """Update the ground tiles to scroll."""
        # Move tiles to the left
        for tile in self.tiles:
            tile.center_x -= speed * delta_time
            tile.update_animation(delta_time)  # Update animation frame

        # Recycle tiles when they go off-screen
        for tile in self.tiles:
            if tile.right < 0:  # Tile is off the left edge
                tile.center_x += len(self.tiles) * self.tile_width  # Move to the far right

    def draw(self):
        """Draw the ground tiles."""
        self.tiles.draw()
