import os
import pygame
import numpy as np

HOUSE = 1
ROAD = 2
TREE = 3
START = 4
EXIT = 5
AMMO = 6

MAP_HEIGHT = 10
MAP_WIDTH = 40

MAP_NUMBER = 10

main_dir = os.path.split(os.path.abspath(__file__))[0]
map_name = "../csv_maps/desert_" + str(MAP_NUMBER) + ".csv"
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
    building = load_image("desert_building.png")
    building_rect = building.get_rect()
    exit = load_image("exit.png")
    exit_rect = exit.get_rect()
    ammo = load_image("desert_ammo.png")
    ammo_rect = ammo.get_rect()
    cactus = load_image("desert_cactus.png")
    cactus_rect = cactus.get_rect()
    ground = load_image("desert_ground.png")
    ground_rect = ground.get_rect()
    road = load_image("desert_road.png")
    road_rect = road.get_rect()

    for i in range(10):
        for j in range(40):
            top = i * 30
            left = j * 30
            value = data[i][j]

            ground_rect.top = top
            ground_rect.left = left
            screen.blit(ground, ground_rect)
            if value == 1:
                building_rect.top = top
                building_rect.left = left
                screen.blit(building, building_rect)
            elif value == 2:
                road_rect.top = top
                road_rect.left = left
                screen.blit(road, road_rect)
            elif value == 3:
                cactus_rect.top = top
                cactus_rect.left = left
                screen.blit(cactus, cactus_rect)
            elif value == 5:
                exit_rect.top = top
                exit_rect.left = left
                screen.blit(exit, exit_rect)
            elif value == 6:
                ammo_rect.top = top
                ammo_rect.left = left
                screen.blit(ammo, ammo_rect)

    NAME = "Desert_" + str(MAP_NUMBER)

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
