#!/usr/bin/env python
"""
Tank class file
"""

import pygame as pg
from functions import load_image


class Tank(pg.sprite.Sprite):

    def __init__(self, left: int = 0, top: int = 0, fog_of_war: bool = False):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.images = [load_image(im, -1) for im in ("yellow_tank1.png", "yellow_tank2.png")]
        if fog_of_war:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.rect = self.image.get_rect(left=left, top=top)
        self.revealed = False

    def update(self):
        if self.revealed:
            self.image = self.images[1]
