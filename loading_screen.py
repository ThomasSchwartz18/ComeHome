import arcade
import time
from menus.title import Title
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class LoadingScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.loading_start_time = None
        self.loading_duration = 2.0  # Simulate loading time in seconds

    def on_show(self):
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.BLACK)
        self.loading_start_time = time.time()

    def on_draw(self):
        """Draw the loading screen."""
        self.clear()
        arcade.draw_text("Loading...", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Please wait while assets are loaded.",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        progress = (time.time() - self.loading_start_time) / self.loading_duration
        progress = min(progress, 1.0)  # Clamp progress to 1.0
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                                 progress * SCREEN_WIDTH, 20, arcade.color.GREEN)

    def on_update(self, delta_time):
        """Simulate asset loading and transition to Title view."""
        # Simulate loading game assets and leaderboard
        if time.time() - self.loading_start_time >= self.loading_duration:
            # Transition to Title view
            title_view = Title()
            self.window.show_view(title_view)
