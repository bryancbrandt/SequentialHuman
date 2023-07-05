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

        self.baseline_images = []  # the list of images for the current participant
        self.baseline_csv = []  # the list of csv file corresponding to the images
        self.training_images = []
        self.training_csv = []

        # Get the file order number
        self.file_order = locals.anchoring_baseline_order[participant_no]
        baseline = self.file_order[:len(self.file_order) // 2]
        training = self.file_order[len(self.file_order) // 2:]

        # Add the files to the baseline and training lists
        for item in baseline:
            file = locals.anchoring_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.baseline_images.append(file)
            self.baseline_csv.append(file[:-3] + "csv")

        for item in training:
            file = locals.anchoring_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
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


class AnchoringMaskingRandomization:
    def __init__(self, participant_no: int = 0):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Anchoring_Masking")
        self.participant_no = participant_no
        self.masking_png = []
        self.masking_csv = []

        masking_order = locals.anchoring_masking_order[participant_no]

        for item in masking_order:
            file = locals.anchoring_masking_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.masking_png.append(file)
            self.masking_csv.append(file[:-3] + "csv")


class CompromiseBaselineRandomization:
    def __init__(self, participant_no: int = 0):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Compromise_Baseline")
        self.participant_no = participant_no
        self.baseline_png = []
        self.baseline_csv = []
        self.training_png = []
        self.training_csv = []

        self.file_order = locals.compromise_baseline_order[self.participant_no]

        baseline = self.file_order[:len(self.file_order) // 2]
        training = self.file_order[len(self.file_order) // 2:]

        # Add the files to the baseline and training lists
        for item in baseline:
            file = locals.compromise_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.baseline_png.append(file)
            self.baseline_csv.append(file[:-3] + "csv")

        for item in training:
            file = locals.compromise_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.training_png.append(file)
            self.training_csv.append(file[:-3] + "csv")


class CompromiseTrainingRandomization():
    def __init__(self, participant_no: int = 0):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Compromise_Training")
        self.participant_no = participant_no
        self.training_png = []
        self.training_csv = []

        self.file_order = locals.compromise_training_order[participant_no]

        for item in self.file_order:
            file = locals.compromise_training_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.training_png.append(file)
            self.training_csv.append(file[:-3] + "csv")

class AttractionBaselineRandomization():
    def __init__(self, participant_no: int = 0):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.join(self.dir_path, "maps/Compromise_Baseline")
        self.participant_no = participant_no
        self.baseline_png = []
        self.baseline_csv = []
        self.training_png = []
        self.training_csv = []

        self.file_order = locals.attraction_baseline_order[self.participant_no]

        baseline = self.file_order[:len(self.file_order) // 2]
        training = self.file_order[len(self.file_order) // 2:]

        # Add the files to the baseline and training lists
        for item in baseline:
            file = locals.attraction_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.baseline_png.append(file)
            self.baseline_csv.append(file[:-3] + "csv")

        for item in training:
            file = locals.attraction_baseline_images[item - 1]
            file = os.path.join(self.dir_path, file)
            self.training_png.append(file)
            self.training_csv.append(file[:-3] + "csv")