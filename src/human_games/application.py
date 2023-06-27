import logging

from PySide6.QtWidgets import QDialog

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
    This is the main application class that exectues the games and the dialog boxes
    """

    def __init__(self):
        super(Application, self).__init__()
        logging.basicConfig(format="%(name)s,%(message)s", level=logging.INFO, filename="participant.log")

        # Enter the participant number dialog box
        self.startDialog = StartDialog(self)
        self.startDialog.setModal(True)
        self.startDialog.show()
        if self.startDialog.exec_():
            logging.info("Participant Dialog Complete.")

        # Begin the tutorials
        self.moveup = TutorialMoveUp()
        self.moveright = TutorialMoveRight()
        self.movedown = TutorialMoveDown()
        self.moveleft = TutorialMoveLeft()
        self.movetank = TutorialTank()
        self.movepowerup = TutorialPowerUp()

        # Demographics and Competencey Ratings Dialogs
        self.demographicsDialog = DemographicsDialog()
        self.demographicsDialog.show()
        if self.demographicsDialog.exec_():
            logging.info("Demographics Dialog complete.")
        self.competenceDialog = CompetenceDialog()
        self.competenceDialog.show()
        if self.competenceDialog.exec_():
            logging.info("Competence Dialog complete.")

        """
        # Game Experience Questionaire Dialog
        self.geqDialog = GEQDialog()
        self.geqDialog.setModal(True)
        self.geqDialog.show()
        if self.geqDialog.exec_():
            logging.info("GEQ Dialog complete.")
        """