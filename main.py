import arcade
from loading_screen import LoadingScreen

class GetOutGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "ComeHome")
        self.loading_screen = LoadingScreen()
        self.show_view(self.loading_screen)  # Show the loading screen immediately

def main():
    # Create the main application window
    window = GetOutGame()
    arcade.run()

if __name__ == "__main__":
    main()
