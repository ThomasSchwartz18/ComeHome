import arcade

class Obstacle(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Animation textures
        self.textures = []
        sprite_sheet_path = "assets/obstacle.png"
        frame_width = 32
        frame_height = 32
        frame_count = 5

        # Load frames from the sprite sheet
        for i in range(frame_count):
            x_frame = i * frame_width
            texture = arcade.load_texture(
                sprite_sheet_path,
                x=x_frame,
                y=0,
                width=frame_width,
                height=frame_height
            )
            self.textures.append(texture)
            
        # Initial speed
        self.initial_speed = -5  # Obstacles start at -5 speed
        self.change_x = self.initial_speed  # Set the starting speed

        # Set the first texture
        self.texture = self.textures[0]
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.frame_duration = 0.1  # Seconds per frame

        # Set position
        self.center_x = x
        self.center_y = y

    def update_animation(self, delta_time):
        """Update the obstacle animation."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]

    def update(self, running_speed):
        """Move the obstacle based on the current running speed."""
        # Update speed dynamically based on the running speed of the player
        self.change_x = self.initial_speed - (running_speed / 100)  # Adjust speed proportionally
        
        self.center_x += self.change_x  # Update position

        # Update animation
        self.update_animation(1 / 60)  # Assuming 60 FPS
