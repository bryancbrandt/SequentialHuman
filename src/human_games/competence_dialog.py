"""
Class file for the competence dialog box
"""
import logging
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QLabel, QSlider, QDialog)


class Ui_Competency(object):
    def setupUi(self, Competency):
        if not Competency.objectName():
            Competency.setObjectName(u"Competency")
        Competency.resize(599, 349)
        self.buttonBox = QDialogButtonBox(Competency)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(240, 310, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.lblGameExperience = QLabel(Competency)
        self.lblGameExperience.setObjectName(u"lblGameExperience")
        self.lblGameExperience.setGeometry(QRect(10, 10, 581, 31))
        self.sliderExperience = QSlider(Competency)
        self.sliderExperience.setObjectName(u"sliderExperience")
        self.sliderExperience.setGeometry(QRect(10, 40, 561, 22))
        self.sliderExperience.setMinimum(1)
        self.sliderExperience.setMaximum(10)
        self.sliderExperience.setSingleStep(1)
        self.sliderExperience.setOrientation(Qt.Horizontal)
        self.sliderExperience.setTickPosition(QSlider.TicksBelow)
        self.sliderExperience.setTickInterval(1)
        self.lbl_Experience_Numbers = QLabel(Competency)
        self.lbl_Experience_Numbers.setObjectName(u"lbl_Experience_Numbers")
        self.lbl_Experience_Numbers.setGeometry(QRect(10, 60, 570, 16))
        self.lblGameControls = QLabel(Competency)
        self.lblGameControls.setObjectName(u"lblGameControls")
        self.lblGameControls.setGeometry(QRect(10, 120, 581, 31))
        self.sliderControls = QSlider(Competency)
        self.sliderControls.setObjectName(u"sliderControls")
        self.sliderControls.setGeometry(QRect(10, 150, 561, 22))
        self.sliderControls.setMinimum(1)
        self.sliderControls.setMaximum(10)
        self.sliderControls.setSingleStep(1)
        self.sliderControls.setOrientation(Qt.Horizontal)
        self.sliderControls.setTickPosition(QSlider.TicksBelow)
        self.sliderControls.setTickInterval(1)
        self.lbl_Controls_Numbers = QLabel(Competency)
        self.lbl_Controls_Numbers.setObjectName(u"lbl_Controls_Numbers")
        self.lbl_Controls_Numbers.setGeometry(QRect(10, 170, 570, 16))
        self.lblTasks = QLabel(Competency)
        self.lblTasks.setObjectName(u"lblTasks")
        self.lblTasks.setGeometry(QRect(10, 220, 591, 31))
        self.sliderTasks = QSlider(Competency)
        self.sliderTasks.setObjectName(u"sliderTasks")
        self.sliderTasks.setGeometry(QRect(10, 250, 561, 22))
        self.sliderTasks.setMinimum(1)
        self.sliderTasks.setMaximum(10)
        self.sliderTasks.setSingleStep(1)
        self.sliderTasks.setOrientation(Qt.Horizontal)
        self.sliderTasks.setTickPosition(QSlider.TicksBelow)
        self.sliderTasks.setTickInterval(1)
        self.lbl_Tasks_Numbers = QLabel(Competency)
        self.lbl_Tasks_Numbers.setObjectName(u"lbl_Tasks_Numbers")
        self.lbl_Tasks_Numbers.setGeometry(QRect(10, 270, 570, 16))

        self.retranslateUi(Competency)
        self.buttonBox.accepted.connect(Competency.accept)
        self.buttonBox.rejected.connect(Competency.reject)

        QMetaObject.connectSlotsByName(Competency)

    # setupUi

    def retranslateUi(self, Competency):
        Competency.setWindowTitle(QCoreApplication.translate("Competency", u"Comp", None))
        self.lblGameExperience.setText(QCoreApplication.translate("Competency",
                                                                  u"On a scale of 1 to 10 (1 = experience, 10 = play everyday) how experienced are you at playing video games?",
                                                                  None))
        self.lbl_Experience_Numbers.setText(QCoreApplication.translate("Competency",
                                                                       u"1                   2                   3                  4                   5                  6                  7                   8                  9                  10 ",
                                                                       None))
        self.lblGameControls.setText(QCoreApplication.translate("Competency",
                                                                u"On a scale of 1 to 10 (1 = none, 10 = absolute) how well do you understand the controls of the game?",
                                                                None))
        self.lbl_Controls_Numbers.setText(QCoreApplication.translate("Competency",
                                                                     u"1                   2                   3                  4                   5                  6                  7                   8                  9                  10 ",
                                                                     None))
        self.lblTasks.setText(QCoreApplication.translate("Competency",
                                                         u"On a scale of 1 to 10 (1 = nonee, 10 = absolute) how confident are you that you can complete the games tasks?",
                                                         None))
        self.lbl_Tasks_Numbers.setText(QCoreApplication.translate("Competency",
                                                                  u"1                   2                   3                  4                   5                  6                  7                   8                  9                  10 ",
                                                                  None))


class CompetenceDialog(QDialog):
    def __init__(self, parent):
        super(CompetenceDialog, self).__init__(parent)
        self.ui = Ui_Competency()
        self.ui.setupUi(self)
        self.logger = logging.getLogger("Competence")

    def accept(self) -> None:
        self.logger.info(f"Experience: {self.ui.sliderExperience.value()}")
        self.logger.info(f"Controls: {self.ui.sliderControls.value()}")
        self.logger.info(f"Tasks: {self.ui.sliderTasks.value()}")
        self.done(1)

    def reject(self) -> None:
        pass
