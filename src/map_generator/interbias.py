import os

import numpy
import pygame
import numpy as np
import typing

from src.human_games.locals import compromise_state_to_rowcol

TANK = 1
JET = 2
GROUND = 3
CACTUS = 4
ROCK = 5
BUSH = 6

MAP_HEIGHT = 20
MAP_WIDTH = 20

MAP_NUMBER = 20
NUMBER_OF_TANKS = np.random.randint(5, 25, dtype=int)
NUMBER_OF_JETS = np.random.randint(5, 25, dtype=int)

main_dir = os.path.split(os.path.abspath(__file__))[0]
map_name = "../csv_maps/interbias.csv"
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


def generate_fillers(num_items: int = 20, type_of_graphic: int = TANK) -> typing.List:
    """
    Generates random graphics on the map by setting matrix values in the data table
    :param num_items: the number of items to generate
    :param type_of_graphic: the type of graphic to be drawn
    :return:
    """
    count = 0
    while count < num_items:
        rnd = int(np.random.randint(0, 400, 1, int))
        row_col = compromise_state_to_rowcol(rnd)
        if not data[row_col[0]][row_col[1]] == TANK:
            if not data[row_col[0]][row_col[1]] == JET:
                if not data[row_col[0]][row_col[1]] == CACTUS:
                    if not data[row_col[0]][row_col[1]] == ROCK:
                        if not data[row_col[0]][row_col[1]] == BUSH:
                            data[row_col[0]][row_col[1]] = type_of_graphic
                            count += 1


def main():
    pygame.init()

    screen = pygame.display.set_mode((MAP_WIDTH * 30, MAP_HEIGHT * 30))

    tank = load_image("orange_tank.png")
    tank_rect = tank.get_rect()
    jet = load_image("orange_jet.png")
    jet_rect = jet.get_rect()
    ground = load_image("desert_ground.png")
    ground_rect = ground.get_rect()
    cactus = load_image("desert_cactus.png")
    cactus_rect = cactus.get_rect()
    rock = load_image("desert_rock.png")
    rock_rect = rock.get_rect()
    bush = load_image("desert_bush.png")
    bush_rect = bush.get_rect()

    generate_fillers(NUMBER_OF_TANKS, TANK)
    generate_fillers(NUMBER_OF_JETS, JET)

    unique, counts = numpy.unique(data, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    objects_to_generate = counts_dict[0.0]

    number_of_rocks = 20
    number_of_cactus = ((objects_to_generate - number_of_rocks) / 2) - 70
    number_of_bushes = ((objects_to_generate - number_of_rocks) / 2) - 95

    assert number_of_rocks > 0
    assert number_of_bushes > 0
    assert number_of_cactus > 0

    generate_fillers(number_of_rocks, ROCK)
    generate_fillers(number_of_cactus, CACTUS)
    generate_fillers(number_of_bushes, BUSH)

    for i in range(20):
        for j in range(20):
            top = i * 30
            left = j * 30
            value = data[i][j]

            ground_rect.top = top
            ground_rect.left = left
            screen.blit(ground, ground_rect)
            if value == TANK:
                tank_rect.top = top
                tank_rect.left = left
                screen.blit(tank, tank_rect)
            elif value == JET:
                jet_rect.top = top
                jet_rect.left = left
                screen.blit(jet, jet_rect)
            elif value == CACTUS:
                cactus_rect.top = top
                cactus_rect.left = left
                screen.blit(cactus, cactus_rect)
            elif value == ROCK:
                rock_rect.top = top
                rock_rect.left = left
                screen.blit(rock, rock_rect)
            elif value == BUSH:
                bush_rect.top = top
                bush_rect.left = left
                screen.blit(bush, bush_rect)

    NAME = "interbias_" + str(MAP_NUMBER)

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
