import arcade
from core.loading_screen import LoadingScreen
from utils.util import BackgroundMusicManager

class ComeHomeGame(arcade.Window):
    def __init__(self):
        super().__init__(1200, 800, "ComeHome")
        
        # Set up custom cursor
        self.set_mouse_visible(False)
        try:
            self.custom_cursor = arcade.Sprite("assets/images/game/cursor.png", scale=1.25)
            self.cursor_width = self.custom_cursor.width
            self.cursor_height = self.custom_cursor.height
            print("Custom cursor loaded successfully.")
        except Exception as e:
            print(f"Error loading custom cursor: {e}")
            self.custom_cursor = None

        # Show the initial loading screen
        self.loading_screen = LoadingScreen()
        self.show_view(self.loading_screen)

        # Initialize the background music manager
        self.music_manager = BackgroundMusicManager("assets/sounds/background/GuitarStrum.wav")
        self.music_manager.play_music()

    def on_draw(self):
        # Ensure the current view's draw method is called
        super().on_draw()

        # Draw the custom cursor
        if self.custom_cursor:
            # Offset the cursor's position so that the (0,0) point of the image aligns with the mouse
            self.custom_cursor.center_x = self._mouse_x + self.cursor_width / 2
            self.custom_cursor.center_y = self._mouse_y - self.cursor_height / 2
            self.custom_cursor.draw()

    def on_update(self, delta_time):
        """Global updates, including background music volume adjustment."""
        self.music_manager.update_volume(delta_time)

def main():
    # Create the main application window
    window = ComeHomeGame()
    arcade.run()

if __name__ == "__main__":
    main()
