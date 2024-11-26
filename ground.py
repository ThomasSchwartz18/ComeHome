import arcade
from constants import GROUND_HEIGHT, SCREEN_WIDTH

class Ground:
    def __init__(self):
        self.tiles = arcade.SpriteList()

        # Path to the ground tile texture
        ground_texture_path = "assets/tiles/GroundTile.png"

        # Load the texture
        ground_texture = arcade.load_texture(ground_texture_path)

        # Tile dimensions
        self.tile_width = 64
        self.tile_height = 100

        # Create and position tiles for an extra screen width
        for x in range(0, SCREEN_WIDTH * 2, self.tile_width):
            tile = arcade.Sprite()
            tile.texture = ground_texture
            tile.width = self.tile_width
            tile.height = self.tile_height
            tile.center_x = x
            tile.center_y = GROUND_HEIGHT // 2
            self.tiles.append(tile)

    def update(self, delta_time, speed):
        """Update the ground tiles to scroll."""
        # Move tiles to the left
        for tile in self.tiles:
            tile.center_x -= speed * delta_time

        # Recycle tiles when they go off-screen
        for tile in self.tiles:
            if tile.right < 0:  # Tile is off the left edge
                tile.center_x += len(self.tiles) * self.tile_width  # Move to the far right

    def draw(self):
        """Draw the ground tiles."""
        self.tiles.draw()
