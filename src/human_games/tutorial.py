import os
import numpy as np
import logging
import pygame as pg
import ctypes
from powerup import PowerUp
from tank import Tank
from player import Player
from explosion import Explosion
from pygame.locals import *


class Tutorial():

    def __init__(self, map_name: str, display_height: int, display_width: int):
        assert os.path.isfile(map_name), f"ERROR! map : {map_name} does not exist"
        self.data = np.genfromtxt(map_name, delimiter=",")

        # Declare object values for identification from the data array
        self.EXIT = 5
        self.AMMO = 6
        self.TANK = 9
        self.PLAYER = 4

        # Initialize pygame basics
        pg.init()
        self.screen = pg.display.set_mode((display_height, display_width))
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()
        self.clock = pg.time.Clock()

        # Game Groups
        self.tanks = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates()

        # Assign groups to sprite classes
        Explosion.containers = self.all, self.tanks
        Tank.containers = self.all
        Player.containers = self.all
        PowerUp.containers = self.all


class TutorialMoveUp(Tutorial):

    def __init__(self):
        map_name = "./maps/Tutorial/tutorial_up.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_up.png")
        super().__init__(map_name, 600, 600)
        self.logger = logging.getLogger("TutorialMoveUp")
        player_position = np.where(self.data == self.PLAYER)
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]

        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "Welcome to the game! \n\n" + \
               "You are the commander of a drone swarm, illustrated by the group of triangles you will see in the " \
               "center of the screen.\n\n" + \
               "We will first begin by practicing some movements to show you how to navigate the maps. \n\n" + \
               "Press the up arrow key to move the drones to the exit point pictured above the drone swarm."
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    if event.key == K_UP:
                        self.player.moveup()

                    if event.key == K_LEFT:
                        self.player.moveleft()

                    if event.key == K_DOWN:
                        self.player.movedown()

            self.all.update()

            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                self.logger.info("Level Completed.")
                return


class TutorialMoveRight(Tutorial):

    def __init__(self, ):
        map_name = "./maps/Tutorial/tutorial_right.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_right.png")
        super().__init__(map_name, 600, 600)
        self.logger = logging.getLogger("TutorialMoveRight")
        player_position = np.where(self.data == self.PLAYER)
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]
        self.all.update()
        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "Great Job! \n\n" + \
               "Now move the drone swarm to the right towards the exit.\n\n"
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    if event.key == K_UP:
                        self.player.moveup()

                    if event.key == K_LEFT:
                        self.player.moveleft()

                    if event.key == K_DOWN:
                        self.player.movedown()

            self.all.update()
            self.screen.blit(self.background_image, (0, 0))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                self.logger.info("Level Completed.")
                return


class TutorialMoveDown(Tutorial):

    def __init__(self, ):
        map_name = "./maps/Tutorial/tutorial_down.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_down.png")
        super().__init__(map_name, 600, 600)
        self.logger = logging.getLogger("TutorialMoveDown")
        player_position = np.where(self.data == self.PLAYER)
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]

        self.all.update()
        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "Excellent Work! \n\n" + \
               "Now move the drone swarm down towards the exit.\n\n"
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    if event.key == K_UP:
                        self.player.moveup()

                    if event.key == K_LEFT:
                        self.player.moveleft()

                    if event.key == K_DOWN:
                        self.player.movedown()

            self.all.update()
            self.screen.blit(self.background_image, (0, 0))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                self.logger.info("Level Completed.")
                return


class TutorialMoveLeft(Tutorial):

    def __init__(self, ):
        map_name = "./maps/Tutorial/tutorial_left.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_left.png")
        super().__init__(map_name, 600, 600)
        self.logger = logging.getLogger("TutorialMoveLeft")
        player_position = np.where(self.data == self.PLAYER)
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]

        self.all.update()
        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "Nice! \n\n" + \
               "Now move the drone swarm to the left towards the exit.\n\n"
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    if event.key == K_UP:
                        self.player.moveup()

                    if event.key == K_LEFT:
                        self.player.moveleft()

                    if event.key == K_DOWN:
                        self.player.movedown()

            self.all.update()
            self.screen.blit(self.background_image, (0, 0))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                self.logger.info("Level Completed.")
                return


class TutorialTank(Tutorial):

    def __init__(self, ):
        map_name = "./maps/Tutorial/tutorial_tank.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_tank.png")
        super().__init__(map_name, 600, 630)
        self.logger = logging.getLogger("TutorialTank")
        player_position = np.where(self.data == self.PLAYER)

        # Get the start locations of the player, exit, and tanks
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]

        pg.draw.rect(self.screen, (255, 255, 255), (0, 600, 600, 30))

        self.score = 0
        self.ammo = 100
        self.score_font = pg.font.SysFont("comicsans", 22, True)
        self.ammo_font = pg.font.SysFont("comicsans", 22, True)

        tank_positions = np.where(self.data == self.TANK)
        tank_positions = list(zip(tank_positions[0], tank_positions[1]))
        self.tank_list = []
        for items in tank_positions:
            self.tank_list.append(Tank(items[0] * 30, items[1] * 30))

        self.all.update()
        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "In the next tutorial we will learn about destroying enemies. \n\n" + \
               "Some levels will require you to destroy the yellow tanks on the map.\n\n" + \
               "Sometimes these tanks will be visible, sometimes they will not. \n\n" + \
               "The information given before the level will let you know if the level\n" \
               "contains hidden or visible tanks.\n\n" + \
               "The primary purpose of this map is to familiarize you with the range of your weapons. \n\n" + \
               "Your mission is to destroy all the tanks, and then navigate to the exit to finish the level.\n\n" + \
               "You can fire your weapons by pressing the space bar.  If you are close \n" + \
               "enough, the tank will explode, and will be eliminated from the map.\n\n" + \
               "You will not be able to exit until all of the tanks have been destroyed.\n\n" + \
               "You will also notice a white bar at the bottom of the screen.  This is the status bar.  " + \
               "  It contains the information for your score and your ammunition.\n\n  When you destroy a tank" + \
               "your score will increase by 100 points.\n\n" + \
               "Additonally, when you fire your weapon, your ammunition will decrease by one."
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    if event.key == K_UP:
                        self.player.moveup()

                    if event.key == K_LEFT:
                        self.player.moveleft()

                    if event.key == K_DOWN:
                        self.player.movedown()

                    if event.key == K_SPACE:
                        self.ammo -= 1
                        for tank in self.tank_list:
                            if self.player.fire(tank):
                                Explosion(tank)
                                tank.kill()
                                self.tank_list.remove(tank)
                                self.score += 100

            self.all.update()

            score_label = self.score_font.render("Score: " + str(self.score), 1, (250, 0, 0))
            ammo_label = self.ammo_font.render("Ammo: " + str(self.ammo), 1, (250, 0, 0))

            self.screen.blit(self.background_image, (0, 0))
            pg.draw.rect(self.screen, (255, 255, 255), (0, 600, 600, 30))
            self.screen.blit(score_label, (30, 600))
            self.screen.blit(ammo_label, (300, 600))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                if len(self.tank_list) <= 0:
                    self.logger.info("Level Completed.")
                    return


class TutorialPowerUp(Tutorial):

    def __init__(self, ):
        map_name = "./maps/Tutorial/tutorial_powerup.csv"
        self.background_image = pg.image.load("./maps/Tutorial/tutorial_powerup.png")
        super().__init__(map_name, 600, 630)
        self.logger = logging.getLogger("TutorialPowerUp")
        player_position = np.where(self.data == self.PLAYER)

        self.score = 0
        self.ammo = 0
        self.score_font = pg.font.SysFont("comicsans", 22, True)
        self.ammo_font = pg.font.SysFont("comicsans", 22, True)

        # Get the start locations of the player, exit, and tanks
        self.player = Player(player_position[0][0], player_position[1][0])
        self.exit_location = np.where(self.data == self.EXIT)
        self.exit_location = [self.exit_location[0][0], self.exit_location[1][0]]

        self.powerup_positions = np.where(self.data == self.AMMO)
        self.powerup_positions = list(zip(self.powerup_positions[0], self.powerup_positions[1]))

        # Draw the scorebar
        pg.draw.rect(self.screen, (255, 255, 255), (0, 600, 600, 30))

        self.all.update()
        self.screen.blit(self.background_image, (0, 0))
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)
        pg.display.flip()

        text = "In the next tutorial we will learn about picking up power-ups. \n\n" + \
               "Power-ups refill your ammunition.\n\n" + \
               "Once you have picked up a power-up the color of the power-up \n" + \
               "will change, indicating that it has been spent.\n\n" + \
               "You can pick up a power-up by navigating to the spot that it is located in.\n\n" + \
               "You will notice when you pick up a power-up, your ammunition on the score bar increases\n\n" + \
               "To complete the level, navigate the map, and pick up all the power-ups."
        ctypes.windll.user32.MessageBoxW(0, text, "Tutorial Introduction", 0)

        while True:
            self.clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.moveright()
                        self.draw_powerup()

                    if event.key == K_UP:
                        self.player.moveup()
                        self.draw_powerup()

                    if event.key == K_LEFT:
                        self.player.moveleft()
                        self.draw_powerup()

                    if event.key == K_DOWN:
                        self.player.movedown()
                        self.draw_powerup()

            self.all.update()
            score_label = self.score_font.render("Score: " + str(self.score), 1, (250, 0, 0))
            ammo_label = self.ammo_font.render("Ammo: " + str(self.ammo), 1, (250, 0, 0))

            self.screen.blit(self.background_image, (0, 0))
            pg.draw.rect(self.screen, (255, 255, 255), (0, 600, 600, 30))
            self.screen.blit(score_label, (30, 600))
            self.screen.blit(ammo_label, (300, 600))
            dirty = self.all.draw(self.screen)
            pg.display.update(dirty)
            pg.display.flip()
            if self.player.pos == self.exit_location:
                if len(self.powerup_positions) <= 0:
                    self.logger.info("Level Completed.")
                    return

    def draw_powerup(self):

        for items in self.powerup_positions:
            if self.player.pos[0] == items[0] and self.player.pos[1] == items[1]:
                PowerUp(items[1] * 30, items[0] * 30)
                self.powerup_positions.remove(items)
                self.ammo += 100



