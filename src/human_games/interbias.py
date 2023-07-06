import ctypes
import easygui
import logging
import numpy as np
import os
import pygame
import random
import src.human_games.locals
import time


class Interbias:
    def __init__(self, participant_no: int):
        assert isinstance(participant_no, int) and participant_no >= 0, "participant number must be >= 0"

        self.participant_no = participant_no - 1
        self.image_index_list = src.human_games.locals.interbias_order[participant_no]
        self.image_index = 0
        self.logger = logging.getLogger("INTERBIAS")

        # get the image files
        self.frequency_dict = {}
        for file_number in range(1, 21):
            filename = f"interbias_{file_number}.csv"  # Replace with the actual filename format
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dir_path, f"maps/Interbias/{filename}")
            if os.path.exists(file_path):
                data = np.genfromtxt(file_path, delimiter=",")
                count_1 = np.where(data == 1)[0].size
                count_2 = np.where(data == 2)[0].size
                file_path = file_path[:-3] + "png"
                self.frequency_dict[file_number] = {"FILE": file_path, "TANK": count_1, "JET": count_2}

    def show_condition(self, participant_no: int):

        self.logger.info("Condition Initiated")

        # Message Box
        count_type = random.choice(['TANK', 'JET'])
        text = "Your next task is as follows:" + \
               f"You will have 15 seconds to count the number of {count_type}S.\n\n" + \
               "You will then enter your count to see if you guessed correctly!\n\n" + \
               "Your guess will affect your score..."
        ctypes.windll.user32.MessageBoxW(0, text, "Map Choice", 0)

        # Initialize the pygame window
        pygame.init()
        window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Inter-condition")
        image_path = self.frequency_dict[self.image_index_list[self.image_index]]["FILE"]
        image = pygame.image.load(image_path)

        image = image.convert()
        window.blit(image, (0, 0))
        pygame.display.update()

        duration = 15
        start_time = time.time()
        end_time = start_time + duration

        # Start the pygame loop and the timer
        while time.time() < end_time:
            time.sleep(1)
        pygame.quit()

        # Get the count for the correct type (TANK, JET)
        if count_type == "TANK":
            object_count = self.frequency_dict[self.image_index_list[self.image_index]]["TANK"]
        else:
            object_count = self.frequency_dict[self.image_index_list[self.image_index]]["JET"]

        # Display the input box and get user input
        user_input = easygui.enterbox("Enter your guess:", "Counting")
        if user_input is not None:
            if count_type == "TANK":
                if int(user_input) == object_count:
                    self.logger.info(f"Correctly guessed {object_count} Tanks")
                    ctypes.windll.user32.MessageBoxW(0, f"Correctly guessed {object_count} Tanks!", "Map Choice", 0)
                else:
                    self.logger.info(f"Incorrectly guessed {user_input}/{object_count} Tanks")
                    ctypes.windll.user32.MessageBoxW(0, f"Sorry there were {object_count} Tanks", "Map Choice", 0)
            else:
                if int(user_input) == object_count:
                    self.logger.info(f"Correctly guessed {object_count} Jets")
                    ctypes.windll.user32.MessageBoxW(0, f"Correctly guessed {object_count} Jets!", "Map Choice", 0)
                else:
                    self.logger.info(f"Incorrectly guessed {user_input}/{object_count} Tanks")
                    ctypes.windll.user32.MessageBoxW(0, f"Sorry there were {object_count} Jets", "Map Choice", 0)
        self.image_index += 1
