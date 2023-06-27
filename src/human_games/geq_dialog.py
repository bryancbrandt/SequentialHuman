"""
Class for the Game Experience Questionnaire Compact version
"""
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,QLabel,  QSlider)


class Ui_GEQ(object):
    def setupUi(self, GEQ):
        if not GEQ.objectName():
            GEQ.setObjectName(u"GEQ")
        GEQ.resize(812, 633)
        self.buttonBox = QDialogButtonBox(GEQ)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(460, 600, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.label = QLabel(GEQ)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 521, 16))
        self.label_2 = QLabel(GEQ)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 40, 351, 16))
        self.label_3 = QLabel(GEQ)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 60, 351, 16))
        self.label1 = QLabel(GEQ)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(20, 90, 81, 16))
        self.label2 = QLabel(GEQ)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(20, 120, 81, 16))
        self.Slider1 = QSlider(GEQ)
        self.Slider1.setObjectName(u"Slider1")
        self.Slider1.setGeometry(QRect(220, 90, 160, 22))
        self.Slider1.setMaximum(4)
        self.Slider1.setOrientation(Qt.Horizontal)
        self.Slider1.setTickPosition(QSlider.TicksBelow)
        self.Slider1.setTickInterval(1)
        self.Slider2 = QSlider(GEQ)
        self.Slider2.setObjectName(u"Slider2")
        self.Slider2.setGeometry(QRect(220, 120, 160, 22))
        self.Slider2.setMaximum(4)
        self.Slider2.setOrientation(Qt.Horizontal)
        self.Slider2.setTickPosition(QSlider.TicksBelow)
        self.Slider2.setTickInterval(1)
        self.Slider4 = QSlider(GEQ)
        self.Slider4.setObjectName(u"Slider4")
        self.Slider4.setGeometry(QRect(220, 180, 160, 22))
        self.Slider4.setMaximum(4)
        self.Slider4.setOrientation(Qt.Horizontal)
        self.Slider4.setTickPosition(QSlider.TicksBelow)
        self.Slider4.setTickInterval(1)
        self.Slider3 = QSlider(GEQ)
        self.Slider3.setObjectName(u"Slider3")
        self.Slider3.setGeometry(QRect(220, 150, 160, 22))
        self.Slider3.setMaximum(4)
        self.Slider3.setOrientation(Qt.Horizontal)
        self.Slider3.setTickPosition(QSlider.TicksBelow)
        self.Slider3.setTickInterval(1)
        self.Slider8 = QSlider(GEQ)
        self.Slider8.setObjectName(u"Slider8")
        self.Slider8.setGeometry(QRect(220, 300, 160, 22))
        self.Slider8.setMaximum(4)
        self.Slider8.setOrientation(Qt.Horizontal)
        self.Slider8.setTickPosition(QSlider.TicksBelow)
        self.Slider8.setTickInterval(1)
        self.Slider6 = QSlider(GEQ)
        self.Slider6.setObjectName(u"Slider6")
        self.Slider6.setGeometry(QRect(220, 240, 160, 22))
        self.Slider6.setMaximum(4)
        self.Slider6.setOrientation(Qt.Horizontal)
        self.Slider6.setTickPosition(QSlider.TicksBelow)
        self.Slider6.setTickInterval(1)
        self.Slider7 = QSlider(GEQ)
        self.Slider7.setObjectName(u"Slider7")
        self.Slider7.setGeometry(QRect(220, 270, 160, 22))
        self.Slider7.setMaximum(4)
        self.Slider7.setOrientation(Qt.Horizontal)
        self.Slider7.setTickPosition(QSlider.TicksBelow)
        self.Slider7.setTickInterval(1)
        self.Slider5 = QSlider(GEQ)
        self.Slider5.setObjectName(u"Slider5")
        self.Slider5.setGeometry(QRect(220, 210, 160, 22))
        self.Slider5.setMaximum(4)
        self.Slider5.setOrientation(Qt.Horizontal)
        self.Slider5.setTickPosition(QSlider.TicksBelow)
        self.Slider5.setTickInterval(1)
        self.Slider15 = QSlider(GEQ)
        self.Slider15.setObjectName(u"Slider15")
        self.Slider15.setGeometry(QRect(220, 510, 160, 22))
        self.Slider15.setMaximum(4)
        self.Slider15.setOrientation(Qt.Horizontal)
        self.Slider15.setTickPosition(QSlider.TicksBelow)
        self.Slider15.setTickInterval(1)
        self.Slider12 = QSlider(GEQ)
        self.Slider12.setObjectName(u"Slider12")
        self.Slider12.setGeometry(QRect(220, 420, 160, 22))
        self.Slider12.setMaximum(4)
        self.Slider12.setOrientation(Qt.Horizontal)
        self.Slider12.setTickPosition(QSlider.TicksBelow)
        self.Slider12.setTickInterval(1)
        self.Slider10 = QSlider(GEQ)
        self.Slider10.setObjectName(u"Slider10")
        self.Slider10.setGeometry(QRect(220, 360, 160, 22))
        self.Slider10.setMaximum(4)
        self.Slider10.setOrientation(Qt.Horizontal)
        self.Slider10.setTickPosition(QSlider.TicksBelow)
        self.Slider10.setTickInterval(1)
        self.Slider11 = QSlider(GEQ)
        self.Slider11.setObjectName(u"Slider11")
        self.Slider11.setGeometry(QRect(220, 390, 160, 22))
        self.Slider11.setMaximum(4)
        self.Slider11.setOrientation(Qt.Horizontal)
        self.Slider11.setTickPosition(QSlider.TicksBelow)
        self.Slider11.setTickInterval(1)
        self.Slider13 = QSlider(GEQ)
        self.Slider13.setObjectName(u"Slider13")
        self.Slider13.setGeometry(QRect(220, 450, 160, 22))
        self.Slider13.setMaximum(4)
        self.Slider13.setOrientation(Qt.Horizontal)
        self.Slider13.setTickPosition(QSlider.TicksBelow)
        self.Slider13.setTickInterval(1)
        self.Slider16 = QSlider(GEQ)
        self.Slider16.setObjectName(u"Slider16")
        self.Slider16.setGeometry(QRect(220, 540, 160, 22))
        self.Slider16.setMaximum(4)
        self.Slider16.setOrientation(Qt.Horizontal)
        self.Slider16.setTickPosition(QSlider.TicksBelow)
        self.Slider16.setTickInterval(1)
        self.Slider9 = QSlider(GEQ)
        self.Slider9.setObjectName(u"Slider9")
        self.Slider9.setGeometry(QRect(220, 330, 160, 22))
        self.Slider9.setMaximum(4)
        self.Slider9.setOrientation(Qt.Horizontal)
        self.Slider9.setTickPosition(QSlider.TicksBelow)
        self.Slider9.setTickInterval(1)
        self.Slider14 = QSlider(GEQ)
        self.Slider14.setObjectName(u"Slider14")
        self.Slider14.setGeometry(QRect(220, 480, 160, 22))
        self.Slider14.setMaximum(4)
        self.Slider14.setOrientation(Qt.Horizontal)
        self.Slider14.setTickPosition(QSlider.TicksBelow)
        self.Slider14.setTickInterval(1)
        self.label4 = QLabel(GEQ)
        self.label4.setObjectName(u"label4")
        self.label4.setGeometry(QRect(20, 180, 131, 16))
        self.label3 = QLabel(GEQ)
        self.label3.setObjectName(u"label3")
        self.label3.setGeometry(QRect(20, 150, 161, 16))
        self.label6 = QLabel(GEQ)
        self.label6.setObjectName(u"label6")
        self.label6.setGeometry(QRect(20, 240, 81, 16))
        self.label5 = QLabel(GEQ)
        self.label5.setObjectName(u"label5")
        self.label5.setGeometry(QRect(20, 210, 201, 16))
        self.label12 = QLabel(GEQ)
        self.label12.setObjectName(u"label12")
        self.label12.setGeometry(QRect(20, 420, 171, 16))
        self.label10 = QLabel(GEQ)
        self.label10.setObjectName(u"label10")
        self.label10.setGeometry(QRect(20, 360, 131, 16))
        self.label9 = QLabel(GEQ)
        self.label9.setObjectName(u"label9")
        self.label9.setGeometry(QRect(20, 330, 141, 16))
        self.label8 = QLabel(GEQ)
        self.label8.setObjectName(u"label8")
        self.label8.setGeometry(QRect(20, 300, 171, 16))
        self.label11 = QLabel(GEQ)
        self.label11.setObjectName(u"label11")
        self.label11.setGeometry(QRect(20, 390, 141, 16))
        self.label7 = QLabel(GEQ)
        self.label7.setObjectName(u"label7")
        self.label7.setGeometry(QRect(20, 270, 151, 16))
        self.label14 = QLabel(GEQ)
        self.label14.setObjectName(u"label14")
        self.label14.setGeometry(QRect(20, 480, 81, 16))
        self.label16 = QLabel(GEQ)
        self.label16.setObjectName(u"label16")
        self.label16.setGeometry(QRect(20, 540, 81, 16))
        self.label13 = QLabel(GEQ)
        self.label13.setObjectName(u"label13")
        self.label13.setGeometry(QRect(20, 450, 181, 16))
        self.label15 = QLabel(GEQ)
        self.label15.setObjectName(u"label15")
        self.label15.setGeometry(QRect(20, 510, 111, 16))
        self.label22 = QLabel(GEQ)
        self.label22.setObjectName(u"label22")
        self.label22.setGeometry(QRect(440, 240, 161, 16))
        self.Slider23 = QSlider(GEQ)
        self.Slider23.setObjectName(u"Slider23")
        self.Slider23.setGeometry(QRect(640, 270, 160, 22))
        self.Slider23.setMaximum(4)
        self.Slider23.setOrientation(Qt.Horizontal)
        self.Slider23.setTickPosition(QSlider.TicksBelow)
        self.Slider23.setTickInterval(1)
        self.Slider32 = QSlider(GEQ)
        self.Slider32.setObjectName(u"Slider32")
        self.Slider32.setGeometry(QRect(640, 540, 160, 22))
        self.Slider32.setMaximum(4)
        self.Slider32.setOrientation(Qt.Horizontal)
        self.Slider32.setTickPosition(QSlider.TicksBelow)
        self.Slider32.setTickInterval(1)
        self.label32 = QLabel(GEQ)
        self.label32.setObjectName(u"label32")
        self.label32.setGeometry(QRect(440, 540, 131, 16))
        self.Slider31 = QSlider(GEQ)
        self.Slider31.setObjectName(u"Slider31")
        self.Slider31.setGeometry(QRect(640, 510, 160, 22))
        self.Slider31.setMaximum(4)
        self.Slider31.setOrientation(Qt.Horizontal)
        self.Slider31.setTickPosition(QSlider.TicksBelow)
        self.Slider31.setTickInterval(1)
        self.label30 = QLabel(GEQ)
        self.label30.setObjectName(u"label30")
        self.label30.setGeometry(QRect(440, 480, 161, 16))
        self.Slider26 = QSlider(GEQ)
        self.Slider26.setObjectName(u"Slider26")
        self.Slider26.setGeometry(QRect(640, 360, 160, 22))
        self.Slider26.setMaximum(4)
        self.Slider26.setOrientation(Qt.Horizontal)
        self.Slider26.setTickPosition(QSlider.TicksBelow)
        self.Slider26.setTickInterval(1)
        self.label20 = QLabel(GEQ)
        self.label20.setObjectName(u"label20")
        self.label20.setGeometry(QRect(440, 180, 131, 16))
        self.label23 = QLabel(GEQ)
        self.label23.setObjectName(u"label23")
        self.label23.setGeometry(QRect(440, 270, 151, 16))
        self.Slider29 = QSlider(GEQ)
        self.Slider29.setObjectName(u"Slider29")
        self.Slider29.setGeometry(QRect(640, 450, 160, 22))
        self.Slider29.setMaximum(4)
        self.Slider29.setOrientation(Qt.Horizontal)
        self.Slider29.setTickPosition(QSlider.TicksBelow)
        self.Slider29.setTickInterval(1)
        self.label19 = QLabel(GEQ)
        self.label19.setObjectName(u"label19")
        self.label19.setGeometry(QRect(440, 150, 191, 16))
        self.Slider20 = QSlider(GEQ)
        self.Slider20.setObjectName(u"Slider20")
        self.Slider20.setGeometry(QRect(640, 180, 160, 22))
        self.Slider20.setMaximum(4)
        self.Slider20.setOrientation(Qt.Horizontal)
        self.Slider20.setTickPosition(QSlider.TicksBelow)
        self.Slider20.setTickInterval(1)
        self.Slider18 = QSlider(GEQ)
        self.Slider18.setObjectName(u"Slider18")
        self.Slider18.setGeometry(QRect(640, 120, 160, 22))
        self.Slider18.setMaximum(4)
        self.Slider18.setOrientation(Qt.Horizontal)
        self.Slider18.setTickPosition(QSlider.TicksBelow)
        self.Slider18.setTickInterval(1)
        self.label26 = QLabel(GEQ)
        self.label26.setObjectName(u"label26")
        self.label26.setGeometry(QRect(440, 360, 131, 16))
        self.Slider19 = QSlider(GEQ)
        self.Slider19.setObjectName(u"Slider19")
        self.Slider19.setGeometry(QRect(640, 150, 160, 22))
        self.Slider19.setMaximum(4)
        self.Slider19.setOrientation(Qt.Horizontal)
        self.Slider19.setTickPosition(QSlider.TicksBelow)
        self.Slider19.setTickInterval(1)
        self.Slider21 = QSlider(GEQ)
        self.Slider21.setObjectName(u"Slider21")
        self.Slider21.setGeometry(QRect(640, 210, 160, 22))
        self.Slider21.setMaximum(4)
        self.Slider21.setOrientation(Qt.Horizontal)
        self.Slider21.setTickPosition(QSlider.TicksBelow)
        self.Slider21.setTickInterval(1)
        self.label24 = QLabel(GEQ)
        self.label24.setObjectName(u"label24")
        self.label24.setGeometry(QRect(440, 300, 171, 16))
        self.Slider24 = QSlider(GEQ)
        self.Slider24.setObjectName(u"Slider24")
        self.Slider24.setGeometry(QRect(640, 300, 160, 22))
        self.Slider24.setMaximum(4)
        self.Slider24.setOrientation(Qt.Horizontal)
        self.Slider24.setTickPosition(QSlider.TicksBelow)
        self.Slider24.setTickInterval(1)
        self.Slider17 = QSlider(GEQ)
        self.Slider17.setObjectName(u"Slider17")
        self.Slider17.setGeometry(QRect(640, 90, 160, 22))
        self.Slider17.setMaximum(4)
        self.Slider17.setOrientation(Qt.Horizontal)
        self.Slider17.setTickPosition(QSlider.TicksBelow)
        self.Slider17.setTickInterval(1)
        self.Slider30 = QSlider(GEQ)
        self.Slider30.setObjectName(u"Slider30")
        self.Slider30.setGeometry(QRect(640, 480, 160, 22))
        self.Slider30.setMaximum(4)
        self.Slider30.setOrientation(Qt.Horizontal)
        self.Slider30.setTickPosition(QSlider.TicksBelow)
        self.Slider30.setTickInterval(1)
        self.Slider28 = QSlider(GEQ)
        self.Slider28.setObjectName(u"Slider28")
        self.Slider28.setGeometry(QRect(640, 420, 160, 22))
        self.Slider28.setMaximum(4)
        self.Slider28.setOrientation(Qt.Horizontal)
        self.Slider28.setTickPosition(QSlider.TicksBelow)
        self.Slider28.setTickInterval(1)
        self.label28 = QLabel(GEQ)
        self.label28.setObjectName(u"label28")
        self.label28.setGeometry(QRect(440, 420, 191, 16))
        self.label25 = QLabel(GEQ)
        self.label25.setObjectName(u"label25")
        self.label25.setGeometry(QRect(440, 330, 141, 16))
        self.Slider27 = QSlider(GEQ)
        self.Slider27.setObjectName(u"Slider27")
        self.Slider27.setGeometry(QRect(640, 390, 160, 22))
        self.Slider27.setMaximum(4)
        self.Slider27.setOrientation(Qt.Horizontal)
        self.Slider27.setTickPosition(QSlider.TicksBelow)
        self.Slider27.setTickInterval(1)
        self.label27 = QLabel(GEQ)
        self.label27.setObjectName(u"label27")
        self.label27.setGeometry(QRect(440, 390, 141, 16))
        self.label31 = QLabel(GEQ)
        self.label31.setObjectName(u"label31")
        self.label31.setGeometry(QRect(440, 510, 191, 16))
        self.label18 = QLabel(GEQ)
        self.label18.setObjectName(u"label18")
        self.label18.setGeometry(QRect(440, 120, 151, 16))
        self.label21 = QLabel(GEQ)
        self.label21.setObjectName(u"label21")
        self.label21.setGeometry(QRect(440, 210, 201, 16))
        self.Slider22 = QSlider(GEQ)
        self.Slider22.setObjectName(u"Slider22")
        self.Slider22.setGeometry(QRect(640, 240, 160, 22))
        self.Slider22.setMaximum(4)
        self.Slider22.setOrientation(Qt.Horizontal)
        self.Slider22.setTickPosition(QSlider.TicksBelow)
        self.Slider22.setTickInterval(1)
        self.Slider25 = QSlider(GEQ)
        self.Slider25.setObjectName(u"Slider25")
        self.Slider25.setGeometry(QRect(640, 330, 160, 22))
        self.Slider25.setMaximum(4)
        self.Slider25.setOrientation(Qt.Horizontal)
        self.Slider25.setTickPosition(QSlider.TicksBelow)
        self.Slider25.setTickInterval(1)
        self.label17 = QLabel(GEQ)
        self.label17.setObjectName(u"label17")
        self.label17.setGeometry(QRect(440, 90, 141, 16))
        self.label29 = QLabel(GEQ)
        self.label29.setObjectName(u"label29")
        self.label29.setGeometry(QRect(440, 450, 181, 16))
        self.label33 = QLabel(GEQ)
        self.label33.setObjectName(u"label33")
        self.label33.setGeometry(QRect(440, 570, 131, 16))
        self.Slider33 = QSlider(GEQ)
        self.Slider33.setObjectName(u"Slider33")
        self.Slider33.setGeometry(QRect(640, 570, 160, 22))
        self.Slider33.setMaximum(4)
        self.Slider33.setOrientation(Qt.Horizontal)
        self.Slider33.setTickPosition(QSlider.TicksBelow)
        self.Slider33.setTickInterval(1)

        self.retranslateUi(GEQ)
        self.buttonBox.accepted.connect(GEQ.accept)
        self.buttonBox.rejected.connect(GEQ.reject)

        QMetaObject.connectSlotsByName(GEQ)

    # setupUi

    def retranslateUi(self, GEQ):
        GEQ.setWindowTitle(QCoreApplication.translate("GEQ", u"GEQ", None))
        self.label.setText(QCoreApplication.translate("GEQ",
                                                      u"Please indicae how you felt while playing the game for each of the items, on the following scale:",
                                                      None))
        self.label_2.setText(QCoreApplication.translate("GEQ",
                                                        u"Not at all          Slightly          Moderately          Fairly          Extremely       ",
                                                        None))
        self.label_3.setText(QCoreApplication.translate("GEQ",
                                                        u"       0                       1                        2                      3                      4",
                                                        None))
        self.label1.setText(QCoreApplication.translate("GEQ", u"1 I felt content", None))
        self.label2.setText(QCoreApplication.translate("GEQ", u"2 I felt skillful", None))
        self.label4.setText(QCoreApplication.translate("GEQ", u"4 I though it was fun", None))
        self.label3.setText(QCoreApplication.translate("GEQ", u"3 I was interested in the story", None))
        self.label6.setText(QCoreApplication.translate("GEQ", u"6 I felt happy", None))
        self.label5.setText(QCoreApplication.translate("GEQ", u"5 I was fully occupied with the game", None))
        self.label12.setText(QCoreApplication.translate("GEQ", u"12 It was aesthetically pleasing", None))
        self.label10.setText(QCoreApplication.translate("GEQ", u"10 I felt competent", None))
        self.label9.setText(QCoreApplication.translate("GEQ", u"9  I found it tiresome", None))
        self.label8.setText(QCoreApplication.translate("GEQ", u"8 I thought about other things", None))
        self.label11.setText(QCoreApplication.translate("GEQ", u"11 I thought it was hard", None))
        self.label7.setText(QCoreApplication.translate("GEQ", u"7 It gave me a bad mood", None))
        self.label14.setText(QCoreApplication.translate("GEQ", u"14 I felt good", None))
        self.label16.setText(QCoreApplication.translate("GEQ", u"16 I felt bored", None))
        self.label13.setText(QCoreApplication.translate("GEQ", u"13 I forgot everything around me", None))
        self.label15.setText(QCoreApplication.translate("GEQ", u"15 I was good at it", None))
        self.label22.setText(QCoreApplication.translate("GEQ", u"22 I felt annoyed", None))
        self.label32.setText(QCoreApplication.translate("GEQ", u"32 I felt time pressure", None))
        self.label30.setText(QCoreApplication.translate("GEQ", u"30 It felt like a rich experience", None))
        self.label20.setText(QCoreApplication.translate("GEQ", u"20 I enjoyed it", None))
        self.label23.setText(QCoreApplication.translate("GEQ", u"23 I felt pressured", None))
        self.label19.setText(QCoreApplication.translate("GEQ", u"19 I felt that I could explore things", None))
        self.label26.setText(QCoreApplication.translate("GEQ", u"26 I felt challenged", None))
        self.label24.setText(QCoreApplication.translate("GEQ", u"24 I felt irritable", None))
        self.label28.setText(QCoreApplication.translate("GEQ", u"28 I was concentrated on the game", None))
        self.label25.setText(QCoreApplication.translate("GEQ", u"25 I lost track of time", None))
        self.label27.setText(QCoreApplication.translate("GEQ", u"27 I found it impressive", None))
        self.label31.setText(QCoreApplication.translate("GEQ", u"31 I lost connection with the world", None))
        self.label18.setText(QCoreApplication.translate("GEQ", u"18 I felt imaginative", None))
        self.label21.setText(QCoreApplication.translate("GEQ", u"21 I was fast at reaching targets", None))
        self.label17.setText(QCoreApplication.translate("GEQ", u"17 I felt successful", None))
        self.label29.setText(QCoreApplication.translate("GEQ", u"29 I felt frustrated", None))
        self.label33.setText(QCoreApplication.translate("GEQ", u"33 It took a lot of effor", None))


class GEQDialog(QDialog):
    def __init__(self, parent):
        super(GEQDialog, self).__init__(parent)
        self.ui = Ui_GEQ()
        self.ui.setupUi(self)

    def accept(self) -> None:
        pass

    def reject(self) -> None:
        pass

