import random
import math
import arcade
from utils import AnimatedSprite

class LightningBug(AnimatedSprite):
    def __init__(self, x, y, scale=0.5):
        sprite_sheet_path = "assets/world_assets/lightning_bug.png"
        super().__init__(
            sprite_sheet_path=sprite_sheet_path,
            frame_width=32,
            frame_height=32,
            frame_count=6,
            scale=scale,
            frame_duration=0.1
        )

        # Movement properties for sway
        self.base_y = y
        self.sway_angle = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.05, 0.1)
        self.sway_amplitude = random.uniform(5, 6)
        self.float_speed = random.uniform(-4, -2.5)

        # Mirrored texture handling
        self.mirrored_textures = self.generate_mirrored_textures()

        # Set position
        self.center_x = x
        self.center_y = y

    def generate_mirrored_textures(self):
        """Create mirrored versions of all animation frames."""
        mirrored_textures = []
        for i in range(len(self.textures)):
            mirrored_texture = arcade.load_texture(
                self.sprite_sheet_path,  # Use the sprite sheet path
                x=i * self.frame_width,
                y=0,
                width=self.frame_width,
                height=self.frame_height,
                mirrored=True
            )
            mirrored_textures.append(mirrored_texture)
        return mirrored_textures

    def update(self):
        """Move the bug with sway and gentle drift."""
        self.center_x += self.float_speed
        self.sway_angle += self.sway_speed
        self.center_y = self.base_y + math.sin(self.sway_angle) * self.sway_amplitude

        # Update texture based on movement direction
        if self.float_speed > 0:
            self.texture = self.mirrored_textures[self.current_frame]
        else:
            self.texture = self.textures[self.current_frame]

        if self.center_x < -self.width:
            self.remove_from_sprite_lists()
