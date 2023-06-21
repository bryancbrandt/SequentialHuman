import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel, QLineEdit)


class Ui_Demographics(object):
    def setupUi(self, Demographics):
        if not Demographics.objectName():
            Demographics.setObjectName(u"Demographics")
        Demographics.resize(281, 292)
        self.buttonBox = QDialogButtonBox(Demographics)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 250, 261, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.lblAge = QLabel(Demographics)
        self.lblAge.setObjectName(u"lblAge")
        self.lblAge.setGeometry(QRect(10, 10, 121, 16))
        self.lineAge = QLineEdit(Demographics)
        self.lineAge.setObjectName(u"lineAge")
        self.lineAge.setGeometry(QRect(10, 30, 261, 22))
        self.lblGender = QLabel(Demographics)
        self.lblGender.setObjectName(u"lblGender")
        self.lblGender.setGeometry(QRect(10, 70, 141, 16))
        self.lineGender = QLineEdit(Demographics)
        self.lineGender.setObjectName(u"lineGender")
        self.lineGender.setGeometry(QRect(10, 90, 261, 22))
        self.lblMajor = QLabel(Demographics)
        self.lblMajor.setObjectName(u"lblMajor")
        self.lblMajor.setGeometry(QRect(10, 130, 171, 16))
        self.lineMajor = QLineEdit(Demographics)
        self.lineMajor.setObjectName(u"lineMajor")
        self.lineMajor.setGeometry(QRect(10, 150, 261, 22))
        self.lblYearsCollege = QLabel(Demographics)
        self.lblYearsCollege.setObjectName(u"lblYearsCollege")
        self.lblYearsCollege.setGeometry(QRect(10, 190, 231, 16))
        self.lineYearsCollege = QLineEdit(Demographics)
        self.lineYearsCollege.setObjectName(u"lineYearsCollege")
        self.lineYearsCollege.setGeometry(QRect(10, 210, 261, 22))

        self.retranslateUi(Demographics)
        self.buttonBox.accepted.connect(Demographics.accept)
        self.buttonBox.rejected.connect(Demographics.reject)

        QMetaObject.connectSlotsByName(Demographics)

    # setupUi

    def retranslateUi(self, Demographics):
        Demographics.setWindowTitle(QCoreApplication.translate("Demographics", u"Demographics", None))
        self.lblAge.setText(QCoreApplication.translate("Demographics", u"Please enter your age:", None))
        self.lblGender.setText(QCoreApplication.translate("Demographics", u"Please type your gender:", None))
        self.lblMajor.setText(QCoreApplication.translate("Demographics", u"Please type your college major:", None))
        self.lblYearsCollege.setText(
            QCoreApplication.translate("Demographics", u"How many years have you been in college?", None))


class DemographicsDialog(QDialog):
    def __init__(self):
        super(DemographicsDialog, self).__init__()
        self.ui = Ui_Demographics()
        self.ui.setupUi(self)

    def accept(self) -> None:
        pass

    def reject(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DemographicsDialog()
    window.show()

    sys.exit(app.exec())
