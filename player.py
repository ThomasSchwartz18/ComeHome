import arcade
from constants import PLAYER_START_X, PLAYER_START_Y, PLAYER_JUMP_SPEED, GROUND_HEIGHT, PLAYER_GRAVITY

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Animation textures
        self.textures = []
        self.current_frame = 0

        # Load the sprite sheet frames
        sprite_sheet_path = "assets/run_side.png"
        frame_width = 15  # Each frame's width
        frame_height = 15  # Frame height matches the sheet
        frame_count = 8  # Total frames in the sheet

        for i in range(frame_count):
            x = i * frame_width
            try:
                frame = arcade.load_texture(
                    sprite_sheet_path,
                    x=x,
                    y=0,
                    width=frame_width,
                    height=frame_height,
                )
                self.textures.append(frame)
            except Exception as e:
                print(f"Error loading frame {i}: {e}")

        if not self.textures:
            print("No frames loaded. Check your sprite sheet path and dimensions.")
        else:
            print(f"Successfully loaded {len(self.textures)} frames.")


        # Set the initial texture
        self.texture = self.textures[0]

        # Animation speed
        self.animation_speed = 0.1  # Seconds per frame
        self.time_since_last_frame = 0

        # Set up player position and scaling
        self.scale = 2  # Scale the sprite for better visibility
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.change_y = 0

    def update(self):
        """Update the player's position with gravity."""
        # Apply gravity
        self.change_y -= PLAYER_GRAVITY
        self.center_y += self.change_y

        # Prevent the player from falling below the ground
        if self.center_y < GROUND_HEIGHT:
            self.center_y = GROUND_HEIGHT
            self.change_y = 0

    def jump(self):
        """Make the player jump if on the ground."""
        if self.center_y == GROUND_HEIGHT:
            self.change_y = PLAYER_JUMP_SPEED

    def update_animation(self, delta_time):
        """Update the animation based on elapsed time."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            # Update the current frame
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]

