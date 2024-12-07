import arcade

class LevelCreation:
    def __init__(self, level_start, level_end, dialogue, idle_duration):
        self.level_start = level_start
        self.level_end = level_end
        self.dialogue = dialogue
        self.idle_duration = idle_duration
        self.idle_timer = 0  # Track elapsed idle time
        self.is_idle = False  # Track whether the player is currently idle

    def play_intro(self, player):
        """Initiate the intro phase with idle animation and dialogue."""
        self.is_idle = True
        self.idle_timer = 0  # Reset the timer
        player.change_x = 0  # Stop horizontal movement
        player.current_animation = "idle"  # Set the player to idle animation

        # Play dialogue (if provided)
        if self.dialogue:
            try:
                dialogue_sound = arcade.Sound(self.dialogue)
                dialogue_sound.play()
            except Exception as e:
                print(f"Error playing dialogue: {e}")

    def update_intro(self, delta_time, player):
        """Update the idle phase, transitioning back to running after the duration."""
        if self.is_idle:
            self.idle_timer += delta_time
            if self.idle_timer >= self.idle_duration:
                self.is_idle = False  # End the idle phase
                player.current_animation = "running"  # Resume running animation

    def is_level_complete(self, current_distance):
        """Check if the player has reached the end of the level."""
        return current_distance >= self.level_end
