import arcade
import time
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.util import draw_parallax_background


class LoadingScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.loading_start_time = None
        self.loading_duration = 2.0  # Simulate loading time in seconds
        self.assets_loaded = False  # Track if assets are loaded
        self.progress = 0.0  # Progress for the loading bar

        # Background layers
        self.background_layers = []
        self.background_speeds = [0.05, 0.125, 0.25, 0.5]  # Parallax speeds
        self.background_offsets = [0, 0, 0, 0]  # Track each layer's horizontal offset

        # Load the Loading image
        self.loading_image = arcade.load_texture("assets/images/game/menus/Loading.png")

    def on_show(self):
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Load background layers
        for i in range(1, 5):  # Load Background1.png to Background4.png
            layer = arcade.load_texture(f"assets/images/background/Background{i}.png")
            self.background_layers.append(layer)

        self.loading_start_time = time.time()

    def on_draw(self):
        """Draw the loading screen."""
        self.clear()

        # Draw background layers
        draw_parallax_background(
                self.background_layers,
                self.background_offsets,
                self.background_speeds,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
            )
        
        # Draw the Loading image scaled to the window size
        arcade.draw_lrwh_rectangle_textured(
            0,  # X-coordinate (top-left corner of the window)
            0,  # Y-coordinate (top-left corner of the window)
            SCREEN_WIDTH,  # Width of the window
            SCREEN_HEIGHT,  # Height of the window
            self.loading_image
        )

        # Draw the progress bar
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                                     self.progress * SCREEN_WIDTH, 20, arcade.color.GREEN)
        arcade.draw_rectangle_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                                      SCREEN_WIDTH, 20, arcade.color.WHITE)

    def on_update(self, delta_time):
        """Simulate asset loading and transition to the next view."""
        # Scroll the background layers
        for i in range(len(self.background_layers)):
            self.background_offsets[i] += self.background_speeds[i]

        if not self.assets_loaded:
            self.load_assets()
            self.assets_loaded = True

        # Update progress bar
        self.progress = min((time.time() - self.loading_start_time) / self.loading_duration, 1.0)

        # Transition to the next screen when loading is complete
        if self.progress >= 1.0 and self.assets_loaded:
            print("Transitioning to Title view...")
            from menus.title import Title
            title_view = Title()
            self.window.show_view(title_view)

    def load_assets(self):
        """Load game assets."""
        try:
            print("Loading assets...")
            # Simulate loading assets (add actual asset loading here)
            arcade.load_texture("assets/images/background/Background1.png")
            arcade.load_texture("assets/images/background/Background2.png")
            arcade.load_texture("assets/images/background/Background3.png")
            arcade.load_texture("assets/images/background/Background4.png")
            arcade.load_texture("assets/images/characters/jump.png")
            arcade.load_texture("assets/images/characters/run_side.png")
            arcade.load_texture("assets/images/characters/run.png")
            arcade.load_texture("assets/images/game/menus/GameOver.png")
            arcade.load_texture("assets/images/game/menus/Loading.png")
            arcade.load_texture("assets/images/game/menus/TitleMenu-title.png")
            arcade.load_texture("assets/images/game/cursor.png")
            arcade.load_texture("assets/images/world_assets/tiles/GroundTile_Sprite.png")
            arcade.load_texture("assets/images/world_assets/coin.png")
            arcade.load_texture("assets/images/world_assets/lightning_bug.png")
            arcade.load_texture("assets/images/world_assets/obstacle.png")
            arcade.Sound("assets/sounds/background/forest_noises.wav")
            arcade.Sound("assets/sounds/background/GuitarStrum.wav")
            arcade.Sound("assets/sounds/background/wind.wav")
            arcade.Sound("assets/sounds/characters/running.wav")
            arcade.Sound("assets/sounds/characters/Narrator1_1.wav")
            arcade.Sound("assets/sounds/characters/Narrator1_2.wav")
            arcade.Sound("assets/sounds/characters/running.wav")
            arcade.Sound("assets/sounds/characters/dialogue/Level1_1.wav")
            arcade.Sound("assets/sounds/characters/dialogue/Level1_2.wav")
            arcade.Sound("assets/sounds/game_sounds/coin_collection.wav")
            arcade.Sound("assets/sounds/game_sounds/jump.wav")
            print("Assets loaded successfully.")
        except Exception as e:
            print(f"Error loading assets: {e}")
