import logging
import sys
import src.human_games.locals

from PySide6.QtWidgets import QDialog

from src.human_games.anchoring import AnchorBaseline, AnchorCondition
from src.human_games.compattract import CompromiseCondition, AttractionCondition
from src.human_games.interbias import Interbias
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
        startDialog = StartDialog(self)
        startDialog.setModal(True)
        startDialog.show()
        if startDialog.exec_():
            self.participant_number = int(startDialog.participant_number)
            self.participant_number = self.participant_number

        # Configure the logger with the participant number
        log_filename = "participant" + str(self.participant_number) + ".log"
        logging.basicConfig(format="%(name)s:%(message)s", level=logging.INFO, filename=log_filename)
        logging.info(f"Participant Number: {self.participant_number}")

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

        interbias = Interbias(self.participant_number)

        select_order = {
            1: AnchorCondition,
            2: CompromiseCondition,
            3: AttractionCondition,
            4: interbias.show_condition
        }

        condition_ordering = src.human_games.locals.condition_order[self.participant_number - 1]
        print(condition_ordering)

        for number in condition_ordering:
            class_type = select_order.get(number)
            if class_type:
                class_type(self.participant_number)
            else:
                print(f"No class defined for number: {number}")

        # Game Experience Questionnaire Dialog
        geqDialog = GEQDialog(parent=self)
        geqDialog.setModal(True)
        geqDialog.show()
        if geqDialog.exec_():
            logging.info("GEQ Dialog complete.")

        sys.exit()
