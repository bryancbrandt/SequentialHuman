#!/usr/bin/env python
"""
This class manages the graphics and the movement of the graphics for the player
"""
import logging
import numpy as np
import pygame as pg
import pygame.display
from functions import load_image


class Player(pg.sprite.Sprite):
    """ The player is represented as a drone swarm"""
    RADAR_RANGE = 300
    FIRING_RANGE = 90

    def __init__(self, start_top: int = 0, start_left: int = 0, max_top: int = 20, max_left: int = 20) -> None:
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image("drone_swarm.png")
        self.rect = self.image.get_rect(top=start_top*30, left=start_left*30)
        self.pos = [start_top, start_left]  # [row, col]
        self.max_top = max_top
        self.max_left = max_left
        self.area = pg.display.get_surface().get_rect()
        self.logger = logging.getLogger("Player")

        # Radar is the rectangle for revealing enemies hidden from the fog of war.
        # If the rects overlap, the enemy is revealed
        self.radar = pg.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        self.radar.width = self.RADAR_RANGE
        self.radar.height = self.RADAR_RANGE

        # Firing range is the rectangle of the firing range of the player
        self.firing_range = pg.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        self.firing_range.width = self.FIRING_RANGE
        self.firing_range.height = self.FIRING_RANGE

    def moveright(self) -> None:
        if self.pos[1] + 1 < self.max_left:
            self.pos[1] += 1
            self.rect.move_ip(30, 0)
            if not self.area.contains(self.rect):
                self.rect.move_ip(-30, 0)
            self.radar.center = self.rect.center
            self.firing_range.center = self.rect.center

    def movedown(self) -> None:
        if self.pos[0] + 1 < self.max_top:
            self.pos[0] += 1
            self.rect.move_ip(0, 30)
            if not self.area.contains(self.rect):
                self.rect.move_ip(0, -30)
            self.radar.center = self.rect.center
            self.firing_range.center = self.rect.center

    def moveleft(self) -> None:
        if self.pos[1] - 1 >= 0:
            self.pos[1] -= 1
            self.rect.move_ip(-30, 0)
            if not self.area.contains(self.rect):
                self.rect.move_ip(30, 0)
            self.radar.center = self.rect.center
            self.firing_range.center = self.rect.center

    def moveup(self) -> None:
        if self.pos[0] - 1 >= 0:
            self.pos[0] -= 1
            self.rect.move_ip(0, -30)
            if not self.area.contains(self.rect):
                self.rect.move_ip(0, 30)
            self.radar.center = self.rect.center
            self.firing_range.center = self.rect.center

    def fire(self, target: pygame.sprite.Sprite) -> bool:
        return self.firing_range.colliderect(target.rect)

    def fog_of_war(self, target: pygame.sprite.Sprite) -> bool:
        return self.radar.colliderect(target.rect)
