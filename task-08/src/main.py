import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PySide6.QtGui import QMovie
from PySide6.QtCore import Slot
from search_window import SearchWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex")
        self.window = SplashScreen(self)
        self.setCentralWidget(self.window)
        self.setFixedSize(960, 540)
        self.show()

    # It is recommended to use slots whenever we are connecting functions to signals
    @Slot()
    def open_search_window(self):
        self.setWindowTitle("Pokesearch")
        self.window = SearchWindow()
        self.setCentralWidget(self.window)
        self.setFixedSize(750, 450)
        self.show()


class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setStyleSheet(
            """
            QPushButton {
                background-color: dark-grey;
                color: white;
                border: 1px solid #02fdfe;
                font: bold 16px;
                text-align: center;
                border-radius: 10px;
            }
            QMainWindow {
                background-color: black;
            }
            QLabel {
                font-size: 32px;
            }
            QPushButton:hover {
                background-color: #02fdfe;
                color: dark-grey;
            }
        """
        )

        labelmov = QLabel(self)
        splash = QMovie("assets/splash.gif")
        labelmov.setGeometry(0, 0, 960, 540)
        labelmov.setMovie(splash)
        splash.start()

        title_css = "color: white; font-size: 32px; font-weight: 600; font-family: 'Helvetica', 'Arial'"
        poke_search_label = QLabel("POKÉSEARCH", self)
        poke_search_label.setStyleSheet(title_css)
        poke_search_label.setGeometry(50, 15, 900, 250)

        poke_label = QLabel("ENGINE ", self)
        poke_label.setStyleSheet(title_css)
        poke_label.setGeometry(50, 60, 900, 250)

        pushButton = QPushButton(text="GO!", parent=self)
        pushButton.setGeometry(50, 450, 160, 43)
        pushButton.clicked.connect(self.parent.open_search_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
