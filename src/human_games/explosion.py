#!/usr/bin/env python
"""
Explosion Animation Class File
"""

import pygame as pg
from functions import load_image


class Explosion(pg.sprite.Sprite):
    images = []
    defaultlife = 1

    def __init__(self, actor):  # , actor
        pg.sprite.Sprite.__init__(self, self.containers)
        self.images = [load_image(im, -1) for im in ("explo1.png", "explo2.png", "explo3.png",
                                                     "explo4.png", "explo5.png", "explo6.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)  # center=actor.rect.center()
        self.life = self.defaultlife

    def update(self):
        # if the animation is done, kill the image
        if self.life >= 6:
            self.kill()
        else:
            self.image = self.images[self.life]
            self.life = self.life + 1


