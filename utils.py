import arcade

def draw_parallax_background(layers, offsets, speeds, screen_width, screen_height, delta_time=0):
    """Draw and optionally update a parallax background."""
    for i, layer in enumerate(layers):
        offset = offsets[i] % screen_width
        arcade.draw_lrwh_rectangle_textured(-offset, 0, screen_width, screen_height, layer)
        arcade.draw_lrwh_rectangle_textured(screen_width - offset, 0, screen_width, screen_height, layer)
        if delta_time > 0:
            offsets[i] += speeds[i] * delta_time

class AnimatedSprite(arcade.Sprite):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, frame_count, scale=1.0, frame_duration=0.1):
        super().__init__()
        self.textures = []
        self.sprite_sheet_path = sprite_sheet_path
        self.frame_width = frame_width  # Save frame width as instance attribute
        self.frame_height = frame_height  # Save frame height as instance attribute
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0

        # Load frames from the sprite sheet
        for i in range(frame_count):
            x_frame = i * frame_width
            texture = arcade.load_texture(
                sprite_sheet_path,
                x=x_frame,
                y=0,
                width=frame_width,
                height=frame_height,
            )
            self.textures.append(texture)

        # Set the first texture
        self.texture = self.textures[self.current_frame]
        self.scale = scale

    def update_animation(self, delta_time):
        """Update animation frame."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]