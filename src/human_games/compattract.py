import ctypes
import logging
import os
import timeit

import numpy as np
import pygame as pg
from pygame.locals import *

from src.human_games.condition_randomization import CompromiseBaselineRandomization, CompromiseTrainingRandomization, \
    AttractionBaselineRandomization, AttractionTrainingRandomization
from src.human_games.player import Player
from src.human_games.powerup import PowerUp

GRASS = 0
ROCK = 1
ROAD = 2
TALL_GRASS = 3
START = 4
AMMO = 6
EXIT_A = 10
EXIT_B = 11
EXIT_C = 12
EXIT_D = 13


def check_movement(data: np.ndarray, current_pos: np.ndarray, movement: str,
                   max_state_width: int, max_state_height: int) -> bool:
    movement_list = {
        "UP": np.array([-1, 0]),  # 1
        "DOWN": np.array([1, 0]),  # 3
        "LEFT": np.array([0, -1]),  # 2
        "RIGHT": np.array([0, 1])  # 0
    }
    assert movement in movement_list.keys(), "ERROR: Move is not in list of possible moves"
    position = current_pos + movement_list[movement]
    if position[1] < max_state_width and position[0] < max_state_height:
        object_id = data[position[0]][position[1]]
        if object_id == ROCK:
            return False
        elif object_id == TALL_GRASS:
            return False
        elif object_id == START:
            return False
        elif object_id == GRASS:
            return False
        else:
            return True
    else:
        return False


class CompAttractBase:
    def __init__(self, map_name: str, background_image: str, map_height: int = 600, map_width: int = 600,
                 condition_name: str = "", first: bool = False) -> None:
        assert os.path.isfile(map_name), f"ERROR! map: {map_name} does not exist"
        assert os.path.isfile(background_image), f"ERROR! image: {background_image} not found!"
        assert isinstance(map_height, int) and map_height > 0, "map_height should be an integer greater than  0"
        assert isinstance(map_width, int) and map_width > 0, "map_width should be an integer greater than 0"
        assert isinstance(condition_name, str) and len(
            condition_name) > 0, "condition_name should be a non-empty string"
        assert isinstance(first, bool), "first should be a boolean"
        # Declare object values for identification from the data array
        self.MAP_NAME = map_name
        self.MAP_HEIGHT = map_height
        self.MAP_WIDTH = map_width
        self.CONDITION_NAME = condition_name

        # Assign class attributes
        self.data = np.genfromtxt(map_name, delimiter=",")
        self.background_image = pg.image.load(background_image)
        self.logger = logging.getLogger(condition_name)
        self.first_condition = first

        self.actions = []
        self.MAX_STATE_WIDTH = 20
        self.MAX_STATE_HEIGHT = 20

        # Initialize pygame and other settings
        pg.init()
        self.screen = pg.display.set_mode((self.MAP_WIDTH, self.MAP_HEIGHT))
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()
        self.clock = pg.time.Clock()

        # Create Game Groups
        self.tanks = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates()

        # Assign groups to sprite classes
        Player.containers = self.all
        PowerUp.containers = self.all

        # Get the player position
        player_position = np.where(self.data == START)
        self.player = Player(player_position[0][0], player_position[1][0], 21, 40)

        # Get the exit position
        self.exit_location = {"A": [np.where(self.data == EXIT_A)[0][0], np.where(self.data == EXIT_A)[1][0]],
                              "B": [np.where(self.data == EXIT_B)[0][0], np.where(self.data == EXIT_B)[1][0]]}
        if np.any(np.where(self.data == EXIT_C)):
            self.exit_location["C"] = [np.where(self.data == EXIT_C)[0][0], np.where(self.data == EXIT_C)[1][0]]
        if np.any(np.where(self.data == EXIT_D)):
            self.exit_location["D"] = [np.where(self.data == EXIT_D)[0][0], np.where(self.data == EXIT_D)[1][0]]

        # Get the power up positions
        self.powerup_positions = np.where(self.data == AMMO)
        self.powerup_positions = list(zip(self.powerup_positions[0], self.powerup_positions[1]))

        # Update the display
        self.all.update()
        self.screen.blit(self.background, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

    def run_game_loop(self, condition_text: str = ""):
        """
        This method prints the message passed in condition text to a system message box to provide instructions
        for the task, then starts the game loop.  The method terminates when the player has finished the level's goals.
        :param condition_text:
        :return:
        """
        # If this is the first condition, display the message text
        if self.first_condition:
            ctypes.windll.user32.MessageBoxW(0, condition_text, "Map Choice", 0)

        self.logger.info(f"MapName: {self.MAP_NAME}")
        self.logger.info(f"Condition Begins: {timeit.default_timer()}")

        # Start the game loop
        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == K_RIGHT:
                        self.logger.info(f"RightKey:{timeit.default_timer()}")
                        self.actions.append(0)
                        if check_movement(self.data, np.array(self.player.pos), "RIGHT",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveright()
                        self.check_powerup()

                    if event.key == K_UP:
                        self.logger.info(f"UpKey:{timeit.default_timer()}")
                        self.actions.append(1)
                        if check_movement(self.data, np.array(self.player.pos), "UP",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveup()
                        self.check_powerup()

                    if event.key == K_LEFT:
                        self.logger.info(f"LeftKey:{timeit.default_timer()}")
                        self.actions.append(2)
                        if check_movement(self.data, np.array(self.player.pos), "LEFT",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveleft()
                        self.check_powerup()

                    if event.key == K_DOWN:
                        self.logger.info(f"DownKey:{timeit.default_timer()}")
                        self.actions.append(3)
                        if check_movement(self.data, np.array(self.player.pos), "DOWN",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.movedown()
                        self.check_powerup()

            self.all.update()

            self.screen.blit(self.background_image, (0, 0))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos in self.exit_location.values():
                self.logger.info(
                    f"Exit Chosen: {[key for key, value in self.exit_location.items() if value == self.player.pos]}")
                self.logger.info(f"Actions:{self.actions}")
                self.logger.info("Level Completed.")
                return

    def check_powerup(self):
        self.draw_powerup()

    def draw_powerup(self):
        for items in self.powerup_positions:
            if self.player.pos[0] == items[0] and self.player.pos[1] == items[1]:
                self.logger.info(f"PowerUp Reached: {timeit.default_timer()}")
                PowerUp(items[1] * 30, items[0] * 30)
                self.powerup_positions.remove(items)


class CompromiseBaseline(CompAttractBase):
    def __init__(self, map_name: str, background_image: str, first: bool):
        text = "Welcome to this level!\n\n" + \
               "Your task is to choose which path to navigate.\n\n" + \
               "One of the exits has more power-ups than the other.\n\n" + \
               "The longer the path, the more likely the enemy will discover you.\n\n " + \
               "However, you can significantly increase your ammo with power-ups.\n\n" + \
               "Your choices will not affect your score.\n\n" + \
               "Good luck!"
        super().__init__(map_name, background_image, 600, 600, "CompromiseBaseline", first)
        self.run_game_loop(text)


class CompromiseTraining(CompAttractBase):
    def __init__(self, map_name: str, background_image: str, first: bool):
        text = "Welcome to this level!\n\n" + \
               "Your task is to choose 1 of the 3 paths to navigate.\n\n" + \
               "Some exits have more power-ups than others.\n\n" + \
               "The paths that are longer, when taken, increase the chance you will be " + \
               "discovered by the enemy.  The shorter paths have a lower chance of enemy discovery.\n\n" + \
               "However, you can significantly increase your ammo with power-ups.\n\n" + \
               "Your choices here will not affect your overall score!\n\n" + \
               "Good luck!"
        super().__init__(map_name, background_image, 600, 600, "CompromiseTraining", first)
        self.run_game_loop(text)


class AttractionBaseline(CompAttractBase):
    def __init__(self, map_name: str, background_image: str, first: bool):
        text = "Welcome to this level!\n\n" + \
               "Your task is to choose one of the two paths to navigate towards the exit.\n\n" + \
               "One of the exits has more power-ups than the other.\n\n" + \
               "The longer the path, the more likely you will be discovered by the enemy.\n\n" + \
               "However, you can significantly increase your ammo with power-ups.\n\n" + \
               "Your choices will not affect your score.\n\n" + \
               "Good luck!"
        super().__init__(map_name, background_image, 600, 600, "AttractionBaseline", first)
        self.run_game_loop(text)


class AttractionTraining(CompAttractBase):
    def __init__(self, map_name: str, background_image: str, first: bool):
        text = "Welcome to the next level \n\n" + \
               "Your task is to choose one of the three paths to exit the map.\n\n" + \
               "The longer the path, the more likely the enemy will discover you.\n\n" + \
               "However, you can significantly increase your ammo with power-ups.\n\n" + \
               "Your choices, again, will not affect your total score.\n\n" + \
               "Good luck!"
        super().__init__(map_name, background_image, 600, 600, "AttractionTraining", first)
        self.run_game_loop(text)


class CompromiseCondition:
    def __init__(self, participant_no: int):
        self.participant_no = participant_no - 1
        self.rnd_baseline = CompromiseBaselineRandomization(self.participant_no)
        self.rnd_training = CompromiseTrainingRandomization(self.participant_no)
        self.baseline_index = 0
        self.baseline_training_index = 0
        self.training_index = 0

        for i in range(5):
            if self.baseline_index == 0:

                CompromiseBaseline(self.rnd_baseline.baseline_csv[self.baseline_index],
                                   self.rnd_baseline.baseline_png[self.baseline_index],
                                   True)
                self.baseline_index += 1

            else:

                CompromiseBaseline(self.rnd_baseline.baseline_csv[self.baseline_index],
                                   self.rnd_baseline.baseline_png[self.baseline_index],
                                   False)
                self.baseline_index += 1

        for i in range(5):
            if self.training_index == 0:

                CompromiseTraining(self.rnd_training.training_csv[self.training_index],
                                   self.rnd_training.training_png[self.training_index],
                                   True)
                self.training_index += 1

                CompromiseBaseline(self.rnd_baseline.training_csv[self.baseline_training_index],
                                   self.rnd_baseline.training_png[self.baseline_training_index],
                                   True)
                self.baseline_training_index += 1

            else:

                CompromiseTraining(self.rnd_training.training_csv[self.training_index],
                                   self.rnd_training.training_png[self.training_index],
                                   False)
                self.training_index += 1

                CompromiseBaseline(self.rnd_baseline.training_csv[self.baseline_training_index],
                                   self.rnd_baseline.training_png[self.baseline_training_index],
                                   False)
                self.baseline_training_index += 1


class AttractionCondition:
    def __init__(self, participant_no: int):
        self.participant_no = participant_no - 1
        self.rnd_baseline = AttractionBaselineRandomization(self.participant_no)
        self.rnd_training = AttractionTrainingRandomization(self.participant_no)
        self.baseline_index = 0
        self.baseline_training_index = 0
        self.training_index = 0

        for i in range(5):
            if self.baseline_index == 0:

                AttractionBaseline(self.rnd_baseline.baseline_csv[self.baseline_index],
                                   self.rnd_baseline.baseline_png[self.baseline_index],
                                   True)
                self.baseline_index += 1

            else:

                AttractionBaseline(self.rnd_baseline.baseline_csv[self.baseline_index],
                                   self.rnd_baseline.baseline_png[self.baseline_index],
                                   False)
                self.baseline_index += 1

        for i in range(5):
            if self.training_index == 0:

                AttractionTraining(self.rnd_training.training_csv[self.training_index],
                                   self.rnd_training.training_png[self.training_index],
                                   True)
                self.training_index += 1

                AttractionBaseline(self.rnd_baseline.training_csv[self.baseline_training_index],
                                   self.rnd_baseline.training_png[self.baseline_training_index],
                                   True)
                self.baseline_training_index += 1

            else:

                AttractionTraining(self.rnd_training.training_csv[self.training_index],
                                   self.rnd_training.training_png[self.training_index],
                                   False)
                self.training_index += 1

                AttractionBaseline(self.rnd_baseline.training_csv[self.baseline_training_index],
                                   self.rnd_baseline.training_png[self.baseline_training_index],
                                   False)
                self.baseline_training_index += 1

