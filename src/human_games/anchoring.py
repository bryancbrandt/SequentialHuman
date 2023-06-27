"""
Class file for the anchoring conditions
"""

import numpy as np
import os.path
import pygame as pg

from src.human_games.condition_randomization import AnchoringBaselineRandomization
from src.human_games.explosion import Explosion
from src.human_games.player import Player
from src.human_games.powerup import PowerUp
from src.human_games.tank import Tank


class Anchoring():

    def __init__(self, map_name: str, display_height: int, display_width: int):
        assert os.path.isfile(map_name), f"ERROR! map: {map_name} does not exist"
        self.data = np.genfromtxt(map_name, delimiter=",")

        # Declare object values for identification from the data array
        self.HOUSE = 1
        self.ROAD = 2
        self.TREE = 3
        self.START = 4
        self.EXIT = 5
        self.ROCK = 6
        self.TANK = 9

        # Initialize pygame basics
        pg.init()
        self.screen = pg.display.set_mode((display_height, display_width))
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()
        self.clock = pg.time.Clock()

        # Create the game sprite groups
        self.tanks = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates

        # Assign groups to sprite classes
        Explosion.containers = self.all, self.tanks
        Tank.containers = self.all
        Player.containers = self.all
        PowerUp.containers = self.all

class AnchorBaseline(Anchoring):

    def __init__(self):
        rnd = AnchoringBaselineRandomization()
