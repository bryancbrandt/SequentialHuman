import os

import numpy as np

import locals


class AnchoringBaselineRandomization:

    def __init__(self, participant_no: int = 1):
        self.count = 1
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Anchoring_Baseline")
        baseline_images = {}

        # Get all the map files from the Anchoring Bias directory
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith('.png'):
                    baseline_images[self.count] = os.path.join(root, file)
                    self.count += 1

        self.baseline_images = []  # the list of images for the current participant
        self.baseline_csv = []  # the list of csv file corresponding to the images
        self.training_images = []
        self.training_csv = []

        # Get the file order number
        self.file_order = locals.get_anchor_baseline_file_order(participant_no)
        training = self.file_order[:len(self.file_order) // 2]
        baseline = self.file_order[len(self.file_order) // 2:]

        # Add the files to the initial baseline list
        for item in baseline:
            file = baseline_images[item]
            self.baseline_images.append(file)
            self.baseline_csv.append(file[:-3] + "csv")

        for item in training:
            file = baseline_images[item]
            self.training_images.append(file)
            self.training_csv.append(file[:-3] + "csv")


rnd = AnchoringBaselineRandomization(0)

