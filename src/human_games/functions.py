#!/usr/bin/env python
"""
Function definition file
"""
import pygame as pg
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file, colorkey=None, sclae=1):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
        surface.convert_alpha()
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()