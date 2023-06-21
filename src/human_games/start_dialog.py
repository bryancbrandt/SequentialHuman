import sys
from PySide6.QtWidgets import QApplication, QDialog

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QLabel, QLineEdit)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(173, 98)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 60, 151, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 161, 16))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 30, 151, 22))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Enter Participant Number:", None))
    # retranslateUi


class StartDialog(QDialog):
    def __init__(self):
        super(StartDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def accept(self) -> None:
        if self.ui.lineEdit.text() != "":
            print(f"Accepted : {self.ui.lineEdit.text()}")
            sys.exit()
        else:
            print("Textbox is empty!")

    def reject(self) -> None:
        print(f"Canceled!")
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = StartDialog()
    window.show()

    sys.exit(app.exec())
