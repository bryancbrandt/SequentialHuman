import os
import typing
import pygame
import numpy as np
from src.human_games.locals import state_to_rowcol

HOUSE = 1
ROAD = 2
TREE = 3
START = 4
EXIT = 5
TANK = 9


MAP_HEIGHT = 10
MAP_WIDTH = 40

URBAN = True
TANK_COUNT = 20
MAP_NUMBER = 5

main_dir = os.path.split(os.path.abspath(__file__))[0]
map_name = "../csv_maps/urban_rural" + str(MAP_NUMBER) + ".csv"
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


def get_tank_states(num_tanks: int = 20) -> typing.List:
    """
    Generates a list of states in [row, column] format for the tanks
    to be placed in
    :type num_tanks: an integer representing the number of tanks to generate
    :return: A list of lists corresponding to the [row, column] for
    each tank location
    """
    states = []
    while len(states) <= num_tanks:
        rnd = int(np.random.randint(0, 400, 1, int))
        row_col = state_to_rowcol(rnd)
        if not data[row_col[0]][row_col[1]] == 1:
            if not data[row_col[0]][row_col[1]] == 3:
                if not row_col[1] == 0:
                    if not row_col[1] == 1:
                        if not row_col[1] == 2:
                            states.append(row_col)
                            data[row_col[0]][row_col[1]] = TANK
    return states


def main():
    pygame.init()

    screen = pygame.display.set_mode((MAP_WIDTH * 30, MAP_HEIGHT * 30))
    house = load_image("house.png")
    house_rect = house.get_rect()
    exit = load_image("exit.png")
    exit_rect = exit.get_rect()
    grass_rural = load_image("grass_rural.png")
    grass_rural_rect = grass_rural.get_rect()
    grass_urban = load_image("grass_urban.png")
    grass_urban_rect = grass_urban.get_rect()
    road_rural = load_image("road_rural.png")
    road_rural_rect = road_rural.get_rect()
    tree_rural = load_image("tree_rural.png")
    tree_rural_rect = tree_rural.get_rect()
    tree_urban = load_image("tree_urban.png")
    tree_urban_rect = tree_urban.get_rect()
    tree_rural2 = load_image("tree_rural2.png")
    tree_rural2_rect = tree_rural2.get_rect()
    tank = load_image("yellow_tank.png")
    tank_rect = tank.get_rect()

    for i in range(10):
        for j in range(40):
            top = i * 30
            left = j * 30
            value = data[i][j]
            if URBAN:
                grass_urban_rect.top = top
                grass_urban_rect.left = left
                screen.blit(grass_urban, grass_urban_rect)
                if value == 0:
                    grass_urban_rect.top = top
                    grass_urban_rect.left = left
                    screen.blit(grass_urban, grass_urban_rect)
                elif value == 1:
                    house_rect.top = top
                    house_rect.left = left
                    screen.blit(house, house_rect)
                elif value == 2:
                    road_rural_rect.top = top
                    road_rural_rect.left = left
                    screen.blit(road_rural, road_rural_rect)
                elif value == 3:
                    tree_urban_rect.top = top
                    tree_urban_rect.left = left
                    screen.blit(tree_urban, tree_urban_rect)
                elif value == 5:
                    exit_rect.top = top
                    exit_rect.left = left
                    screen.blit(exit, exit_rect)
            else:
                # Create a rural map
                grass_rural_rect.top = top
                grass_rural_rect.left = left
                screen.blit(grass_rural, grass_rural_rect)
                if value == 1:
                    tree_rural_rect.top = top
                    tree_rural_rect.left = left
                    screen.blit(tree_rural, tree_rural_rect)
                elif value == 3:
                    tree_rural2_rect.top = top
                    tree_rural2_rect.left = left
                    screen.blit(tree_rural2, tree_rural2_rect)
                elif value == 5:
                    exit_rect.top = top
                    exit_rect.left = left
                    screen.blit(exit, exit_rect)

    if URBAN:
        NAME = "Urban_" + str(TANK_COUNT) + "_" + str(MAP_NUMBER)
    else:
        NAME = "Rural_" + str(TANK_COUNT) + "_" + str(MAP_NUMBER)

    img_name = NAME + ".png"
    pygame.image.save(screen, img_name)

    tanks = get_tank_states(TANK_COUNT)
    for unit in tanks:
        tank_rect.top = unit[0] * 30
        tank_rect.left = unit[1] * 30
        screen.blit(tank, tank_rect)

    csv_name = NAME + ".csv"
    np.savetxt(csv_name, data, delimiter=",")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()


if __name__ == "__main__":
    main()
