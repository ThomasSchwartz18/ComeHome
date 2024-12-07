import arcade
from utils.constants import PLAYER_START_X, PLAYER_START_Y, PLAYER_JUMP_SPEED, GROUND_HEIGHT, PLAYER_GRAVITY

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Running animation textures
        self.running_textures = []
        self.running_frame_count = 8
        self.running_frame_width = 150
        self.running_frame_height = 149
        self.current_frame = 0

        # Jumping animation textures
        self.jumping_textures = []
        self.jumping_frame_count = 2
        self.jumping_frame_width = 150
        self.jumping_frame_height = 149

        # Idle animation textures
        self.idle_textures = []
        self.idle_frame_count = 4  # Total frames in the idle animation
        self.idle_frame_width = 150
        self.idle_frame_height = 149

        # Load the animations
        self.load_running_textures("assets/images/characters/run_side.png")
        self.load_jumping_textures("assets/images/characters/jump.png")
        self.load_idle_textures("assets/images/characters/Idle.png")

        # Set the initial texture
        self.texture = self.running_textures[0]  # Default to running animation

        # Animation speed
        self.animation_speed = 0.08  # Seconds per frame
        self.time_since_last_frame = 0

        # Animation state
        self.current_animation = "running"  # Can be "running", "jumping", or "idle"

        # Set up player position and scaling
        self.scale = 1
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.change_y = 0
        self.change_x = 0

        # Jumping state
        self.jumps_left = 2  # Allow double jumps
        self.jump_speed = PLAYER_JUMP_SPEED

        # Load the running sound
        self.running_sound = arcade.Sound("assets/sounds/characters/running.wav")
        self.running_sound_playing = False  # Track if the sound is already playing

    def load_running_textures(self, sprite_sheet_path):
        """Load textures for the running animation."""
        for i in range(self.running_frame_count):
            x = i * self.running_frame_width
            frame = arcade.load_texture(
                sprite_sheet_path,
                x=x,
                y=0,
                width=self.running_frame_width,
                height=self.running_frame_height,
            )
            self.running_textures.append(frame)

    def load_jumping_textures(self, sprite_sheet_path):
        """Load textures for the jumping animation."""
        for i in range(self.jumping_frame_count):
            x = i * self.jumping_frame_width
            frame = arcade.load_texture(
                sprite_sheet_path,
                x=x,
                y=0,
                width=self.jumping_frame_width,
                height=self.jumping_frame_height,
            )
            self.jumping_textures.append(frame)

    def load_idle_textures(self, sprite_sheet_path):
        """Load textures for the idle animation."""
        for i in range(self.idle_frame_count):
            x = i * self.idle_frame_width
            frame = arcade.load_texture(
                sprite_sheet_path,
                x=x,
                y=0,
                width=self.idle_frame_width,
                height=self.idle_frame_height,
            )
            self.idle_textures.append(frame)

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
            self.jump_audio = arcade.Sound('assets/sounds/game_sounds/jump.wav')
            self.jump_audio.play()
            self.change_y = self.jump_speed
            self.jumps_left -= 1  # Use a jump

    def update_animation(self, delta_time):
        """Update the animation based on elapsed time."""
        self.time_since_last_frame += delta_time

        if self.current_animation == "jumping":
            # Use jumping animation when in the air
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.jumping_textures)
                self.texture = self.jumping_textures[self.current_frame]
        elif self.current_animation == "idle":
            # Use idle animation when idle
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.current_frame]
        else:
            # Default to running animation
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.running_textures)
                self.texture = self.running_textures[self.current_frame]

        # Play or stop the running sound based on movement
        if self.current_animation == "running" and self.change_x != 0:
            if not self.running_sound_playing:
                self.running_sound.play(loop=True)
                self.running_sound_playing = True
        else:
            if self.running_sound_playing:
                self.running_sound_playing = False

    def move(self, change_x):
        """Update the player's horizontal movement."""
        self.change_x = change_x
        self.center_x += self.change_x
