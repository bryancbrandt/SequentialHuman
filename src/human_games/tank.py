#!/usr/bin/env python
"""
Tank class file
"""

import pygame as pg
from functions import load_image


class Tank(pg.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.images = [load_image(im, -1) for im in ("yellow_tank1.png", "yellow_tank2.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect(left=x, top=y)
        self.revealed = False

    def update(self):
        if self.revealed:
            self.image = self.images[1]

