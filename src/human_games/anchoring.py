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
from src.human_games.condition_randomization import AnchoringBaselineRandomization
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


class AnchorBaseline:
    """
    This is the class file for the baseline condition from the Anchoring bias conditions.
    This file is for both the initial baseline, and the baselines that occur during the training.
    """

    def __init__(self, map_name: str, background_image: str, first: bool = False,
                 fog_of_war: bool = True, score: int = 0, ammo: int = 100):
        assert os.path.isfile(map_name), f"ERROR! map: {map_name} does not exist"
        assert os.path.isfile(background_image), f"ERROR! image: {background_image} not found!"

        # Declare object values for identification from the data array
        self.MAP_HEIGHT = 660
        self.MAP_WIDTH = 1200
        self.FOG_OF_WAR = fog_of_war

        # Assign class attributes
        self.data = np.genfromtxt(map_name, delimiter=",")
        self.background_image = pg.image.load(background_image)
        self.logger = logging.getLogger("AnchorBaseline")
        self.first_condition = first
        self.score = score
        self.ammo = ammo
        self.actions = []
        self.MAX_STATE_WIDTH = 40
        self.MAX_STATE_HEIGHT = 21

        # Initialize pygame basics
        pg.init()
        self.screen = pg.display.set_mode((self.MAP_WIDTH, self.MAP_HEIGHT))
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()
        self.clock = pg.time.Clock()

        # Game Groups
        self.tanks = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates()

        # Assign groups to sprite classes
        Explosion.containers = self.all, self.tanks
        Tank.containers = self.all
        Player.containers = self.all
        PowerUp.containers = self.all

        # Get the player, tank, and exit positions
        player_position = np.where(self.data == START)
        self.player = Player(player_position[0][0], player_position[1][0], 21, 40)
        tank_positions = np.where(self.data == TANK)
        tank_positions = list(zip(tank_positions[0], tank_positions[1]))
        self.tank_list = []
        for items in tank_positions:
            self.tank_list.append(Tank(items[1] * 30, items[0] * 30, self.FOG_OF_WAR))
        exit_location = np.where(self.data == EXIT)
        self.exit_location = []
        self.exit_location.append([exit_location[0][0], exit_location[1][0]])
        self.exit_location.append([exit_location[0][1], exit_location[1][1]])

        # Draw the game bar
        # pg.draw.rect(self.screen, (255, 255, 255), (0, 0, 660, 30))
        self.score_font = pg.font.SysFont("comicsans", 22, True)
        self.ammo_font = pg.font.SysFont("comicsans", 22, True)

        # Update the display
        self.all.update()
        self.screen.blit(self.background, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        # If this is the first time in this condition, provide instructions
        if self.first_condition:
            text = "Welcome to this level!\n\n" + \
                   "Your task is to choose which map to navigate, top or bottom.\n\n" + \
                   "Once a choice has been made, you cannot chang your mind\n\n" + \
                   "Whatever choice you make, there are 5 hidden tanks that must be destoryed" + \
                   "before you can exit the map.\n\n" + \
                   "Good luck!"
            ctypes.windll.user32.MessageBoxW(0, text, "Map Choice", 0)

        self.logger.info(f"AnchoringBaselineBegins: {timeit.default_timer()}")
        self.logger.info(f"MapName:{map_name}")
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
                        if self.FOG_OF_WAR:
                            reveal_tank(self.tank_list, self.player)

                    if event.key == K_UP:
                        self.logger.info(f"UpKey:{timeit.default_timer()}")
                        self.actions.append(1)
                        if check_movement(self.data, np.array(self.player.pos), "UP",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveup()
                        if self.FOG_OF_WAR:
                            reveal_tank(self.tank_list, self.player)

                    if event.key == K_LEFT:
                        self.logger.info(f"LeftKey:{timeit.default_timer()}")
                        self.actions.append(2)
                        if check_movement(self.data, np.array(self.player.pos), "LEFT",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.moveleft()
                        if self.FOG_OF_WAR:
                            reveal_tank(self.tank_list, self.player)

                    if event.key == K_DOWN:
                        self.logger.info(f"DownKey:{timeit.default_timer()}")
                        self.actions.append(3)
                        if check_movement(self.data, np.array(self.player.pos), "DOWN",
                                          self.MAX_STATE_WIDTH, self.MAX_STATE_HEIGHT):
                            self.player.movedown()
                        if self.FOG_OF_WAR:
                            reveal_tank(self.tank_list, self.player)

                    if event.key == K_SPACE:
                        self.logger.info(f"SpaceKey:{timeit.default_timer()}")
                        self.actions.append(4)
                        self.ammo -= 1
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
                if len(self.tank_list) <= 5:
                    self.score += 100
                    self.logger.info(f"Actions:{self.actions}")
                    self.logger.info("Level Completed.")
                    return


class AnchorCondition:
    """
    Class file for the entire anchor condition.  Derives the randomized orders for the baseline and
    training conditions.  Then initializes each conditions class, while transferring scores and ammunition.
    """

    def __init__(self):
        self.baseline_index = 0
        self.score = 0
        self.ammo = 100
        self.baseline_rnd = AnchoringBaselineRandomization(0)
        for i in range(5):
            if self.baseline_index == 0:
                base = AnchorBaseline(self.baseline_rnd.baseline_csv[self.baseline_index],
                                      self.baseline_rnd.baseline_images[self.baseline_index],
                                      True, True, self.score, self.ammo)
                self.baseline_index += 1
                self.score += base.score
                self.ammo = base.ammo
            else:
                base = AnchorBaseline(self.baseline_rnd.baseline_csv[self.baseline_index],
                                      self.baseline_rnd.baseline_images[self.baseline_index],
                                      False, True, self.score, self.ammo)
                self.baseline_index += 1
                self.score += base.score
                self.ammo = base.ammo
