import locals
import os


class AnchoringBaselineRandomization:
    """
    This class file is used to extract the randomization and establish what map
    files (images, and csv) that will be used for the inital 5 baseline conditions
    of anchoring condition and the additional 5 baseline conditions during anchoring
    training conditions.
    """
    def __init__(self, participant_no: int = 0):
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

        # Add the files to the baseline and training lists
        for item in baseline:
            file = baseline_images[item]
            self.baseline_images.append(file)
            self.baseline_csv.append(file[:-3] + "csv")

        for item in training:
            file = baseline_images[item]
            self.training_images.append(file)
            self.training_csv.append(file[:-3] + "csv")


class AnchoringTrainingRandomization:
    """
    This class file is used to extract the randomization, and retrieve
    the image and csv files for the urban and rural conditions that
    are part of the anchoring training condition
    """
    def __init__(self, participant_no: int = 0):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Anchoring_Training")
        self.participant_no = participant_no
        self.is_rural_bias = locals.anchoring_rural_bias[participant_no]
        self.is_rural_start = locals.anchoring_rural_start[participant_no]
        self.rural_csv = []
        self.urban_csv = []
        self.urban_png = []
        self.rural_png = []

        # Get the randomized order of images to be displayed for urban and rural
        rural_order = locals.anchoring_rural_order[self.participant_no]
        urban_order = locals.anchoring_urban_order[self.participant_no]

        # Create the lists of the image locations for urban and rural conditions
        for index in rural_order:
            file = locals.anchoring_training_images_rural[index - 1]
            path = os.path.join(self.dir_path, file)
            self.rural_png.append(path)
        for index in urban_order:
            file = locals.anchoring_training_images_urban[index - 1]
            path = os.path.join(self.dir_path, file)
            self.urban_png.append(path)

        # If the bias is for the rural maps, load the corresponding csv files
        # otherwise load the csv files for the bias being the urban maps
        if self.is_rural_bias:
            for index in rural_order:
                file = locals.anchoring_training_csv_rural_bias[1][index - 1]
                path = os.path.join(self.dir_path, file)
                self.rural_csv.append(path)

            for index in urban_order:
                file = locals.anchoring_training_csv_rural_bias[0][index - 1]
                path = os.path.join(self.dir_path, file)
                self.urban_csv.append(path)

        else:
            for index in rural_order:
                file = locals.anchoring_training_csv_urban_bias[1][index - 1]
                path = os.path.join(self.dir_path, file)
                self.rural_csv.append(path)

            for index in urban_order:
                file = locals.anchoring_training_csv_urban_bias[0][index - 1]
                path = os.path.join(self.dir_path, file)
                self.urban_csv.append(path)

