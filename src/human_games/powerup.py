"""
Power-Up class file
"""

import pygame as pg
from locals import load_image


class PowerUp(pg.sprite.Sprite):

    def __init__(self, left: int = 0, top: int = 0):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image("ammo_yellow.png")
        self.rect = self.image.get_rect(left=left, top=top)
