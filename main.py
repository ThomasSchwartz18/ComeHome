import arcade
from loading_screen import LoadingScreen
from utils import BackgroundMusicManager

class ComeHomeGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "ComeHome")
        
        self.loading_screen = LoadingScreen()
        self.show_view(self.loading_screen)  # Show the loading screen immediately

        # Initialize the background music manager
        self.music_manager = BackgroundMusicManager("assets/sounds/background/GuitarStrum.wav")
        self.music_manager.play_music()

    def on_update(self, delta_time):
        """Global updates, including background music volume adjustment."""
        self.music_manager.update_volume(delta_time)

def main():
    # Create the main application window
    window = ComeHomeGame()
    arcade.run()

if __name__ == "__main__":
    main()
