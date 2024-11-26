import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, GROUND_HEIGHT, OBSTACLE_SPAWN_RATE
from player import Player
from obstacle import Obstacle
from ground import Ground
import random
from coin import Coin
import os

class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player = None
        self.ground = None
        self.obstacles = None
        self.score = 0
        self.time_since_last_obstacle = 0
        self.time_since_last_coin = 0
        self.game_over = False
        
        self.coins = arcade.SpriteList()
        self.total_coins_collected = 0

        # Background layers
        self.background_layers = []
        self.background_speeds = [0.2, 0.5, 1.0, 2.0]  # Parallax speeds
        self.background_offsets = [0, 0, 0, 0]  # Track each layer's horizontal offset

    def setup(self):
        # Initialize game objects
        self.ground = Ground()
        self.player = Player()
        self.obstacles = arcade.SpriteList()
        
        # Load the total coins collected
        self.load_total_coins()

        # Load background layers
        for i in range(1, 5):  # Load Background1.png to Background4.png
            layer = arcade.load_texture(f"assets/background/Background{i}.png")
            self.background_layers.append(layer)

    def on_draw(self):
        # Render background layers
        self.clear()
        for i, layer in enumerate(self.background_layers):
            offset = self.background_offsets[i] % SCREEN_WIDTH
            # Draw two copies of the texture side-by-side for seamless scrolling
            arcade.draw_lrwh_rectangle_textured(-offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT, layer)
            arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH - offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT, layer)

        # Render game objects
        self.ground.draw()
        self.player.draw()
        self.obstacles.draw()   
        self.coins.draw()

        # Draw score
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)


    def on_update(self, delta_time):
        if self.game_over:
            print("Game over reached. Saving coins...")
            self.save_total_coins()  # Save total coins collected
            return

        # Update background offsets
        for i in range(len(self.background_layers)):
            self.background_offsets[i] += self.background_speeds[i]

        # Update ground tiles
        ground_scroll_speed = 200  # Pixels per second
        self.ground.update(delta_time, ground_scroll_speed)

        # Update player animation
        self.player.update_animation(delta_time)

        # Update game objects
        self.player.update()
        self.obstacles.update()
        for coin in self.coins:
            coin.update(delta_time, self.player)

        # Update animations
        for obstacle in self.obstacles:
            obstacle.update_animation(delta_time)
        for coin in self.coins:
            coin.update_animation(delta_time)

        # Remove off-screen obstacles
        for obstacle in self.obstacles:
            if obstacle.center_x < -obstacle.width:
                self.obstacles.remove(obstacle)
                self.score += 1

        # Remove off-screen coins
        for coin in self.coins:
            if coin.center_x < -coin.width:
                self.coins.remove(coin)

        # Spawn obstacles periodically
        self.time_since_last_obstacle += delta_time
        if self.time_since_last_obstacle > OBSTACLE_SPAWN_RATE:
            self.time_since_last_obstacle = 0
            self.spawn_obstacle()

        # Spawn coins periodically
        self.time_since_last_coin += delta_time
        if self.time_since_last_coin > 2.0:  # Adjust spawn rate as needed
            self.time_since_last_coin = 0
            self.spawn_coin()

        # Check for collisions with obstacles or coins
        obstacles_hit = arcade.check_for_collision_with_list(self.player, self.obstacles)
        coins_collected = arcade.check_for_collision_with_list(self.player, self.coins)

        if obstacles_hit:
            print("Collision with obstacle detected.")
            print("Setting game_over to True.")
            self.game_over = True
            
            # Save coins before transitioning to the GameOver view
            print("Saving total coins before transitioning.")
            self.save_total_coins()
            
            print("Transitioning to GameOver view.")
            from menus.game_over import GameOver
            game_over_view = GameOver(self.score)
            self.window.show_view(game_over_view)

        for coin in coins_collected:
            self.coins.remove(coin)
            self.total_coins_collected += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player.jump()
        elif key == arcade.key.ESCAPE:
            from menus.pause import Pause
            pause_menu = Pause(self)
            self.window.show_view(pause_menu)

    def spawn_obstacle(self):
        # Create a new animated obstacle
        obstacle = Obstacle(SCREEN_WIDTH, GROUND_HEIGHT + 20)
        self.obstacles.append(obstacle)

    def spawn_coin(self):
        """Spawn a coin at a random position."""
        x = SCREEN_WIDTH  # Spawn at the right edge of the screen
        y = GROUND_HEIGHT + random.randint(20, 50)  # Spawn near the ground with slight variation
        coin = Coin(x, y)
        self.coins.append(coin)

    def load_total_coins(self):
        """Load the total number of coins collected from a file."""
        try:
            with open("game_watcher/total_coins.txt", "r") as file:
                self.total_coins_collected = int(file.read().strip())
        except FileNotFoundError:
            self.total_coins_collected = 0  # Start at 0 if the file doesn't exist

    def save_total_coins(self):
        """Save the total number of coins collected to a file."""
        try:
            # Ensure the directory exists
            os.makedirs("game_watcher", exist_ok=True)

            # Save the total coins to a file
            with open("game_watcher/total_coins.txt", "w") as file:
                file.write(str(self.total_coins_collected))
        except Exception as e:
            print(f"Error saving total coins: {e}")


