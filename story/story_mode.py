import arcade
from story.level_creation import LevelCreation
from core.game_window import GameWindow
import json
import os

def load_story_progress(file_path="game_watcher/story_progress.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default progress if the file doesn't exist
        return {"current_checkpoint": 0, "total_distance": 0}

def save_story_progress(progress, file_path="game_watcher/story_progress.json"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(progress, file)

class StoryMode(GameWindow):
    def __init__(self):
        super().__init__()
        self.story_progress = load_story_progress()
        self.levels = [
            LevelCreation(0, 1000, "assets/sounds/characters/dialogue/level1_1.wav", 10),
            LevelCreation(1000, 2000, "assets/dialogue/level2_intro.wav", 15),
            # Add more levels as needed
        ]
        self.current_level = self.levels[self.story_progress["current_checkpoint"]]

    def setup(self):
        super().setup()
        self.current_level.play_intro(self.player)

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.current_level.is_level_complete(self.score):
            # Advance to the next level
            self.story_progress["current_checkpoint"] += 1
            self.story_progress["total_distance"] = self.score
            save_story_progress(self.story_progress)

            if self.story_progress["current_checkpoint"] < len(self.levels):
                self.current_level = self.levels[self.story_progress["current_checkpoint"]]
                self.setup()  # Reset for the new level
            else:
                print("Story complete!")  # Handle story completion
