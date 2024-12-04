import arcade
from constants import PLAYER_START_X, PLAYER_START_Y, PLAYER_JUMP_SPEED, GROUND_HEIGHT, PLAYER_GRAVITY

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Running animation textures
        self.running_textures = []
        self.running_frame_count = 8  # Total frames in the running animation
        self.running_frame_width = 150  # Width of each frame
        self.running_frame_height = 149  # Height of each frame
        self.current_frame = 0

        # Jumping animation textures
        self.jumping_textures = []
        self.jumping_frame_count = 2  # Total frames in the jump animation
        self.jumping_frame_width = 150  # Width of each jump frame
        self.jumping_frame_height = 149  # Height of each jump frame

        # Load the running animation frames
        self.load_running_textures("assets/run_side.png")

        # Load the jumping animation frames
        self.load_jumping_textures("assets/jump.png")

        # Set the initial texture
        self.texture = self.running_textures[0]  # Default to running animation

        # Animation speed
        self.animation_speed = 0.08  # Seconds per frame
        self.time_since_last_frame = 0

        # Set up player position and scaling
        self.scale = 1  # Scale the sprite for better visibility
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.change_y = 0
        self.change_x = 0

        # Jumping state
        self.jumps_left = 2  # Allow double jumps
        self.jump_speed = PLAYER_JUMP_SPEED

        # Load the running sound
        self.running_sound = arcade.Sound("assets/sounds/character/running.wav")
        self.running_sound_playing = False  # Track if the sound is already playing

    def load_running_textures(self, sprite_sheet_path):
        """Load textures for the running animation."""
        for i in range(self.running_frame_count):
            x = i * self.running_frame_width
            try:
                frame = arcade.load_texture(
                    sprite_sheet_path,
                    x=x,
                    y=0,
                    width=self.running_frame_width,
                    height=self.running_frame_height,
                )
                self.running_textures.append(frame)
            except Exception as e:
                print(f"Error loading running frame {i}: {e}")

        if not self.running_textures:
            print(f"ERROR: No running frames loaded. Check path: {sprite_sheet_path}.")
            raise FileNotFoundError("Running sprite sheet could not be loaded.")

    def load_jumping_textures(self, sprite_sheet_path):
        """Load textures for the jumping animation."""
        for i in range(self.jumping_frame_count):
            x = i * self.jumping_frame_width
            try:
                frame = arcade.load_texture(
                    sprite_sheet_path,
                    x=x,
                    y=0,
                    width=self.jumping_frame_width,
                    height=self.jumping_frame_height,
                )
                self.jumping_textures.append(frame)
            except Exception as e:
                print(f"Error loading jumping frame {i}: {e}")

        if not self.jumping_textures:
            print(f"ERROR: No jumping frames loaded. Check path: {sprite_sheet_path}.")
            raise FileNotFoundError("Jumping sprite sheet could not be loaded.")

    def update(self):
        """Update the player's position with gravity."""
        # Apply gravity
        self.change_y -= PLAYER_GRAVITY
        self.center_y += self.change_y

        # Prevent the player from falling below the ground
        if self.center_y < GROUND_HEIGHT:
            self.center_y = GROUND_HEIGHT
            self.change_y = 0
            self.jumps_left = 2  # Reset jumps when the player lands

    def jump(self):
        """Make the player jump if jumps are available."""
        if self.jumps_left > 0:
            self.jump_audio = arcade.Sound('assets/sounds/game_sounds/jump.mp3')
            self.jump_audio.play()
            self.change_y = self.jump_speed
            self.jumps_left -= 1  # Use a jump

    def update_animation(self, delta_time):
        """Update the animation based on elapsed time."""
        self.time_since_last_frame += delta_time

        # Determine whether to use running or jumping animation
        if self.center_y > GROUND_HEIGHT:
            # Use jumping animation when in the air
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.jumping_textures)
                self.texture = self.jumping_textures[self.current_frame]
        else:
            # Use running animation when on the ground
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.running_textures)
                self.texture = self.running_textures[self.current_frame]

        # Play or stop the running sound based on movement
        if self.center_y == GROUND_HEIGHT and self.change_x != 0:  # Player is running on the ground
            if not self.running_sound_playing:
                self.running_sound.play(loop=True)
                self.running_sound_playing = True
        else:  # Stop the sound if jumping or idle
            if self.running_sound_playing:
                self.running_sound_playing = False

    def move(self, change_x):
        """Update the player's horizontal movement."""
        self.change_x = change_x
        self.center_x += self.change_x
