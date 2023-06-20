import os

import numpy
import pygame
import numpy as np
import typing

from src.human_games.locals import compromise_state_to_rowcol

ROCK = 1
ROAD = 2
TALL_GRASS = 3
START = 4
AMMO = 6
EXIT_A = 10
EXIT_B = 11
EXIT_D = 13

MAP_HEIGHT = 20
MAP_WIDTH = 20

MAP_NUMBER = 5

main_dir = os.path.split(os.path.abspath(__file__))[0]
map_name = "../csv_maps/attraction_training_" + str(MAP_NUMBER) + ".csv"
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


def generate_fillers(num_items: int = 20, type_of_graphic: int = TALL_GRASS) -> typing.List:
    """
    Generates random graphics on the map by setting matrix values in the data table
    :param num_items: the number of items to generate
    :param type_of_graphic: the type of graphic to be drawn
    :return:
    """
    count = 0
    while count <= num_items:
        rnd = int(np.random.randint(0, 400, 1, int))
        row_col = compromise_state_to_rowcol(rnd)
        if not data[row_col[0]][row_col[1]] == ROAD:
            if not data[row_col[0]][row_col[1]] == START:
                if not data[row_col[0]][row_col[1]] == EXIT_A:
                    if not data[row_col[0]][row_col[1]] == EXIT_B:
                        if not data[row_col[0]][row_col[1]] == EXIT_D:
                            if not data[row_col[0]][row_col[1]] == TALL_GRASS:
                                if not data[row_col[0]][row_col[1]] == ROCK:
                                    if not data[row_col[0]][row_col[1]] == AMMO:
                                        data[row_col[0]][row_col[1]] = type_of_graphic
                                        count += 1


def main():
    pygame.init()

    screen = pygame.display.set_mode((MAP_WIDTH * 30, MAP_HEIGHT * 30))
    exit = load_image("exit.png")
    exit_rect = exit.get_rect()
    ammo = load_image("desert_ammo.png")
    ammo_rect = ammo.get_rect()
    ground = load_image("compromise_grass.png")
    ground_rect = ground.get_rect()
    tall_grass = load_image("compromise_tall_grass.png")
    tall_grass_rect = tall_grass.get_rect()
    road = load_image("compromise_road.png")
    road_rect = road.get_rect()
    rock = load_image("compromise_rock.png")
    rock_rect = rock.get_rect()
    start = load_image("compromise_start.png")
    start_rect = start.get_rect()

    unique, counts = numpy.unique(data, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    objects_to_generate = counts_dict[0.0]

    number_of_rocks = 20
    number_of_tall_grass = objects_to_generate - number_of_rocks

    generate_fillers(number_of_tall_grass-10, TALL_GRASS)
    generate_fillers(number_of_rocks, ROCK)

    for i in range(20):
        for j in range(20):
            top = i * 30
            left = j * 30
            value = data[i][j]

            ground_rect.top = top
            ground_rect.left = left
            screen.blit(ground, ground_rect)
            if value == ROCK:
                rock_rect.top = top
                rock_rect.left = left
                screen.blit(rock, rock_rect)
            elif value == ROAD:
                road_rect.top = top
                road_rect.left = left
                screen.blit(road, road_rect)
            elif value == TALL_GRASS:
                tall_grass_rect.top = top
                tall_grass_rect.left = left
                screen.blit(tall_grass, tall_grass_rect)
            elif value == START:
                road_rect.top = top
                road_rect.left = left
                screen.blit(road, road_rect)
                start_rect.top = top
                start_rect.left = left
                screen.blit(start, start_rect)
            elif value == EXIT_A or value == EXIT_B or value == EXIT_D:
                road_rect.top = top
                road_rect.left = left
                screen.blit(road, road_rect)
                exit_rect.top = top
                exit_rect.left = left
                screen.blit(exit, exit_rect)
            elif value == AMMO:
                road_rect.top = top
                road_rect.left = left
                screen.blit(road, road_rect)
                ammo_rect.top = top
                ammo_rect.left = left
                screen.blit(ammo, ammo_rect)

    NAME = "attraction_training_" + str(MAP_NUMBER)

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
