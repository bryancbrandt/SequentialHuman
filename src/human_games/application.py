import logging
import sys

from PySide6.QtWidgets import QDialog

from src.human_games.anchoring import AnchorBaseline, AnchorCondition
from src.human_games.compattract import CompromiseCondition, AttractionCondition
from src.human_games.start_dialog import StartDialog
from src.human_games.demographics_dialog import DemographicsDialog
from src.human_games.competence_dialog import CompetenceDialog
from src.human_games.geq_dialog import GEQDialog
from src.human_games.tutorial import TutorialMoveUp
from src.human_games.tutorial import TutorialMoveRight
from src.human_games.tutorial import TutorialMoveDown
from src.human_games.tutorial import TutorialMoveLeft
from src.human_games.tutorial import TutorialTank
from src.human_games.tutorial import TutorialPowerUp


class Application(QDialog):
    """
    This is the main application class that executes the games and the dialog boxes
    """

    def __init__(self):
        super(Application, self).__init__()

        self.ammo = 100
        self.score = 0

        # Initialize the participant number dialog box, and get the participant number
        self.startDialog = StartDialog(self)
        self.startDialog.setModal(True)
        self.startDialog.show()
        if self.startDialog.exec_():
            self.participant_number = int(self.startDialog.participant_number)

        # Configure the logger with the participant number
        log_filename = "participant" + str(self.participant_number) + ".log"
        logging.basicConfig(format="%(name)s:%(message)s", level=logging.INFO, filename=log_filename)
        logging.info(f"Participant Number: {self.participant_number}")


        """
        # Begin the PyGame tutorials
        TutorialMoveUp()
        TutorialMoveRight()
        TutorialMoveDown()
        TutorialMoveLeft()
        TutorialTank()
        TutorialPowerUp()

        # Demographics and Competence Ratings Dialogs
        self.demographicsDialog = DemographicsDialog(parent=self)
        self.demographicsDialog.show()
        if self.demographicsDialog.exec_():
            logging.info("Demographics Dialog complete.")
        self.competenceDialog = CompetenceDialog(parent=self)
        self.competenceDialog.show()
        if self.competenceDialog.exec_():
            logging.info("Competence Dialog complete.")
        """

        # AnchorCondition(self.participant_number, self.ammo, self.score)
        # CompromiseCondition(self.participant_number)
        AttractionCondition(self.participant_number)
        """
        numbers = [1, 4, 3, 4, 2]
        class_mapping = {
            1: Class1,
            2: Class2,
            3: Class3,
            4: Class4
        }

        instances = []
        for number in numbers:
            class_type = class_mapping.get(number)
            if class_type:
                instance = class_type()
                instances.append(instance)
            else:
                print(f"No class defined for number: {number}")

        # Game Experience Questionnaire Dialog
        self.geqDialog = GEQDialog(parent=self)
        self.geqDialog.setModal(True)
        self.geqDialog.show()
        if self.geqDialog.exec_():
            logging.info("GEQ Dialog complete.")
        """
        sys.exit()
