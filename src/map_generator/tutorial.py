import os

import pygame
import numpy as np

EXIT = 5
AMMO = 6
TANK = 9

MAP_HEIGHT = 20
MAP_WIDTH = 20

MAP_NUMBER = 20

main_dir = os.path.split(os.path.abspath(__file__))[0]
NAME = "tutorial_tank"
map_name = "../csv_maps/" + NAME + ".csv"
data = np.genfromtxt(map_name, delimiter=",")


def load_image(file, colorkey=None, sclae=1):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "graphics", file)
    try:
        surface = pygame.image.load(file)
        surface.convert_alpha()
    except pygame.error:
        raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}')
    return surface.convert_alpha()


def main():
    pygame.init()

    screen = pygame.display.set_mode((MAP_WIDTH * 30, MAP_HEIGHT * 30))

    tank = load_image("yellow_tank.png")
    tank_rect = tank.get_rect()
    ground = load_image("grass_urban.png")
    ground_rect = ground.get_rect()
    start = load_image("compromise_start.png")
    start_rect = start.get_rect()
    exit = load_image("exit.png")
    exit_rect = exit.get_rect()
    ammo = load_image("desert_ammo.png")
    ammo_rect = ammo.get_rect()

    for i in range(20):
        for j in range(20):
            top = i * 30
            left = j * 30
            value = data[i][j]

            ground_rect.top = top
            ground_rect.left = left
            screen.blit(ground, ground_rect)
            if value == EXIT:
                exit_rect.top = top
                exit_rect.left = left
                screen.blit(exit, exit_rect)

    img_name = NAME + ".png"
    pygame.image.save(screen, img_name)

    csv_name = NAME + ".csv"
    np.savetxt(csv_name, data, delimiter=",")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()


if __name__ == "__main__":
    main()
