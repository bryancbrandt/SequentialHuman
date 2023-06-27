"""
Main file that executes the QApplication loop and initializes the application class
"""

import sys
from PySide6.QtWidgets import QApplication
from src.human_games.application import Application


def main():
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
