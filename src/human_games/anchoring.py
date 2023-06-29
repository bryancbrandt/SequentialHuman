"""
Class file for the anchoring conditions
"""
import ctypes
import logging
import numpy as np
import os.path
import pygame as pg
import timeit
import typing
from pygame.locals import *
from src.human_games.condition_randomization import AnchoringBaselineRandomization, AnchoringTrainingRandomization
from src.human_games.explosion import Explosion
from src.human_games.player import Player
from src.human_games.powerup import PowerUp
from src.human_games.tank import Tank

# Constants for object identification on the data numpy array
HOUSE = 1
ROAD = 2
TREE = 3
START = 4
EXIT = 5
ROCK = 6
TANK = 9


def reveal_tank(tanklist: typing.List[Tank], player: Player) -> None:
    """
    Reveals a hidden tank if it within the radar zone of the player
    :param tanklist: The map list containing all the Tank objects
    :param player: The player Object
    :return: None
    """
    for tank in tanklist:
        if player.fog_of_war(tank):
            tank.revealed = True


def check_movement(data: np.ndarray, current_pos: np.ndarray, movement: str,
                   max_state_width: int, max_state_height: int) -> bool:
    """
    Before we move the player graphic, this function ensures that the location the plaer
    is moving to, does not contain an object that the player cannot move upon.
    :param data: The numpy array representing the objects on the map
    :param current_pos: The current position of the player [row, col]
    :param movement: The direction the player is moving in: "RIGHT", "LEFT", etc.
    :param max_state_height:
    :param max_state_width:
    :return: True if the location can be moved to, false otherwise.
    """
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
        if object_id == HOUSE:
            return False
        elif object_id == TREE:
            return False
        elif object_id == ROCK:
            return False
        elif object_id == START:
            return False
        else:
            return True
    else:
        return False


class AnchorBase:
    """
    The base class to be used for all anchor conditions to inherit from
    """

    def __init__(self, map_name: str, background_image: str, score: int = 0, ammo: int = 100,
                 map_height: int = 600, map_width: int = 600, fog_of_war: bool = False,
                 has_power_up: bool = False, has_tanks: bool = True, condition_name: str = "",
                 first: bool = False, exit_threshold: int = 0) -> object:
        assert os.path.isfile(map_name), f"ERROR! map: {map_name} does not exist"
        assert os.path.isfile(background_image), f"ERROR! image: {background_image} not found!"
        assert isinstance(score, int) and score >= 0, "score should be an integer greater than or equal to 0"
        assert isinstance(ammo, int) and ammo >= 0, "ammo should be an integer greater than or equal to 0"
        assert isinstance(map_height, int) and map_height > 0, "map_height should be an integer greater than  0"
        assert isinstance(map_width, int) and map_width > 0, "map_width should be an integer greater than 0"
        assert isinstance(fog_of_war, bool), "fog_of_war should be a boolean"
        assert isinstance(has_power_up, bool), "has_power_up should be a boolean"
        assert isinstance(has_tanks, bool), "has_tanks should be a boolean"
        assert isinstance(condition_name, str) and len(
            condition_name) > 0, "condition_name should be a non-empty string"
        assert isinstance(first, bool), "first should be a boolean"
        assert isinstance(exit_threshold,
                          int) and exit_threshold >= 0, "exit_threshold should be an integer greater than or equal to 0"

        # Declare object values for identification from the data array
        self.MAP_NAME = map_name
        self.MAP_HEIGHT = map_height
        self.MAP_WIDTH = map_width
        self.FOG_OF_WAR = fog_of_war
        self.HAS_POWER_UP = has_power_up
        self.HAS_TANKS = has_tanks
        self.CONDITION_NAME = condition_name

        # Assign class attributes
        self.data = np.genfromtxt(map_name, delimiter=",")
        self.background_image = pg.image.load(background_image)
        self.logger = logging.getLogger(condition_name)
        self.first_condition = first
        self.score = score
        self.ammo = ammo
        self.actions = []
        self.MAX_STATE_WIDTH = self.MAP_WIDTH / 30
        self.MAX_STATE_HEIGHT = (self.MAP_HEIGHT - 30) / 30
        self.EXIT_THRESHOLD = exit_threshold

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
        Explosion.containers = self.all, self.tanks
        Tank.containers = self.all
        Player.containers = self.all
        PowerUp.containers = self.all

        # Get the player position
        player_position = np.where(self.data == START)
        self.player = Player(player_position[0][0], player_position[1][0], 21, 40)

        # Get the exit position
        self.exit_location = []
        locations = np.where(self.data == EXIT)
        array_length = len(locations[0])
        for i in range(array_length):
            pair = list(arr[i] for arr in locations)
            self.exit_location.append(pair)

        # If there are tanks, get their positions
        if self.HAS_TANKS:
            tank_positions = np.where(self.data == TANK)
            tank_positions = list(zip(tank_positions[0], tank_positions[1]))
            self.tank_list = []
            for items in tank_positions:
                self.tank_list.append(Tank(items[1] * 30, items[0] * 30, self.FOG_OF_WAR))

        # If there are power-ups get their positions
        if self.HAS_POWER_UP:
            self.powerup_positions = np.where(self.data == self.AMMO)
            self.powerup_positions = list(zip(self.powerup_positions[0], self.powerup_positions[1]))

        # Draw the game bar
        self.score_font = pg.font.SysFont("comicsans", 22, True)
        self.ammo_font = pg.font.SysFont("comicsans", 22, True)

        # Update the display
        self.all.update()
        self.screen.blit(self.background, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

    def run_game_loop(self, condition_text: str = ""):

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
                        self.check_tanks()
                        self.check_powerup()

                    if event.key == K_UP:
                        self.logger.info(f"UpKey:{timeit.default_timer()}")
                        self.actions.append(1)
                        if check_movement(self.data, np.array(self.player.pos), "UP",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveup()
                        self.check_tanks()
                        self.check_powerup()

                    if event.key == K_LEFT:
                        self.logger.info(f"LeftKey:{timeit.default_timer()}")
                        self.actions.append(2)
                        if check_movement(self.data, np.array(self.player.pos), "LEFT",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveleft()
                        self.check_tanks()
                        self.check_powerup()

                    if event.key == K_DOWN:
                        self.logger.info(f"DownKey:{timeit.default_timer()}")
                        self.actions.append(3)
                        if check_movement(self.data, np.array(self.player.pos), "DOWN",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.movedown()
                        self.check_tanks()
                        self.check_powerup()

                    if event.key == K_SPACE:
                        self.logger.info(f"SpaceKey:{timeit.default_timer()}")
                        self.actions.append(4)
                        self.ammo -= 1
                        if self.HAS_TANKS:
                            for tank in self.tank_list:
                                if self.player.fire(tank):
                                    Explosion(tank)
                                    tank.kill()
                                    self.tank_list.remove(tank)
                                    self.score += 100

            self.all.update()

            score_label = self.score_font.render("Score: " + str(self.score), 1, (250, 0, 0))
            ammo_label = self.ammo_font.render("Ammo: " + str(self.ammo), 1, (250, 0, 0))

            self.screen.blit(self.background_image, (0, 0))
            pg.draw.rect(self.screen, (255, 255, 255), (0, self.MAP_HEIGHT - 30, self.MAP_WIDTH, 30))
            self.screen.blit(score_label, (30, self.MAP_HEIGHT - 30))
            self.screen.blit(ammo_label, (300, self.MAP_HEIGHT - 30))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos in self.exit_location:
                if len(self.tank_list) <= self.EXIT_THRESHOLD:
                    self.score += 100
                    self.logger.info(f"Actions:{self.actions}")
                    self.logger.info("Level Completed.")
                    return

    def check_tanks(self):
        if self.HAS_TANKS:
            if self.FOG_OF_WAR:
                reveal_tank(self.tank_list, self.player)

    def check_powerup(self):
        if self.HAS_POWER_UP:
            self.draw_powerup()

    def draw_powerup(self):
        for items in self.powerup_positions:
            if self.player.pos[0] == items[0] and self.player.pos[1] == items[1]:
                PowerUp(items[1] * 30, items[0] * 30)
                self.powerup_positions.remove(items)
                self.ammo += 100


class AnchorBaseline(AnchorBase):
    def __init__(self, map_name: str, background_image: str, score: int, ammo: int,
                 fog_of_war: bool, first: bool):
        text = "Welcome to this level!\n\n" + \
               "Your task is to choose which map to navigate: top or bottom.\n\n" + \
               "Once a choice has been made, you cannot change your mind.\n\n" + \
               "Whatever choice you make, there are 5 hidden tanks that must be destroyed" + \
               "before you can exit the map.\n\n" + \
               "Good luck!"
        super().__init__(map_name, background_image, score, ammo, 660, 1200,
                         fog_of_war, False, True, "AnchorBaseline", first, 5)
        self.run_game_loop(text)


class AnchorRuralTraining:
    """
    This is the class file for the Rural Training condition from the anchoring bias coniditon
    """
    def __init__(self, map_name: str, background_image: str, score: int = 0, ammo: int = 100,
                 first: bool = False):
        text = "Welcome to the next level! Great work on finishing the previous one!\n\n" +\
            "Your task is to destroy all the tanks on the map.\n\n" +\
            "Good luck!"



class AnchorCondition:
    """
    Class file for the entire anchor condition.  Derives the randomized orders for the baseline and
    training conditions.  Then initializes each conditions class, while transferring scores and ammunition.
    """

    def __init__(self, participant_no: int):
        self.baseline_index = 0
        self.score = 0
        self.ammo = 100
        self.participant_no = participant_no - 1
        self.baseline_rnd = AnchoringBaselineRandomization(self.participant_no)
        self.training_rnd = AnchoringTrainingRandomization(self.participant_no)

        # Run 5 instances of the baseline condition
        for i in range(5):
            if self.baseline_index == 0:
                base = AnchorBaseline(self.baseline_rnd.baseline_csv[self.baseline_index],
                                      self.baseline_rnd.baseline_images[self.baseline_index],
                                      self.score, self.ammo, True, True)
                self.baseline_index += 1
                self.score += base.score
                self.ammo = base.ammo
            else:
                base = AnchorBaseline(self.baseline_rnd.baseline_csv[self.baseline_index],
                                      self.baseline_rnd.baseline_images[self.baseline_index],
                                      self.score, self.ammo, True, False)
                self.baseline_index += 1
                self.score += base.score
                self.ammo = base.ammo
