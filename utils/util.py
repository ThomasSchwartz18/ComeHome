import arcade
import random
import time

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
            
class BackgroundMusicManager:
    def __init__(self, music_file: str):
        """Initialize the background music manager."""
        self.music_file = music_file
        self.background_music = None
        self.background_music_player = None
        self.music_playing = False
        self.music_start_time = None

    def play_music(self):
        """Play the background music with fade-in."""
        if not self.music_playing:
            try:
                self.background_music = arcade.Sound(self.music_file)
                self.music_start_time = time.time()  # Use Python's time module
                self.background_music_player = self.background_music.play(volume=0.0, loop=True)
                self.music_playing = True
            except Exception as e:
                print(f"Error starting background music: {e}")

    def update_volume(self, delta_time):
        """Update the volume of the music for fade-in and fade-out effects."""
        if self.music_playing and self.music_start_time:
            elapsed = time.time() - self.music_start_time  # Calculate elapsed time
            duration = self.background_music.get_length()

            if elapsed < 5:  # Fade in during the first 5 seconds
                self.background_music_player.volume = elapsed / 5
            elif duration - 5 < elapsed < duration:  # Fade out during the last 5 seconds
                self.background_music_player.volume = (duration - elapsed) / 5
            elif elapsed >= duration:  # Loop with delay
                self.stop_music()
                arcade.schedule(self.replay_music, random.uniform(20, 40))

    def replay_music(self, delta_time):
        """Replay the music after a delay."""
        arcade.unschedule(self.replay_music)
        self.play_music()

    def stop_music(self):
        """Stop the background music."""
        if self.music_playing:
            try:
                self.background_music_player.pause()
                self.music_playing = False
            except Exception as e:
                print(f"Error stopping background music: {e}")