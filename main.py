import arcade
from menus.title import Title
from loading_screen import LoadingScreen

def main():
    # Create the main application window
    window = arcade.Window(800, 600, "GetOut")
    loading_screen = LoadingScreen()
    window.show_view(loading_screen)  # Start with the loading screen
    title_view = Title()
    window.show_view(title_view)  # Show the title menu
    arcade.run()

if __name__ == "__main__":
    main()
