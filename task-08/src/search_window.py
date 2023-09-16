from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFrame,
    QDialog,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot
from display_window import DisplayWindow
import requests


class Notification(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification")
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setGeometry(30, 20, 250, 40)
        self.setFixedSize(300, 85)

    def display_notification(self, text):
        self.label.setText(text)
        self.exec()


class SearchWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    @Slot()
    def search(self):
        self._fetch_api()
        self._show_image()
        self._show_stats()

    @Slot()
    def capture(self):
        name = self.response["name"].title()
        self.captured_pokemon.append((name, self.img_data))
        self.notif.display_notification(f"{name} has been captured!")

    @Slot()
    def display(self):
        display = DisplayWindow(self.captured_pokemon)
        display.show()

    def _fetch_api(self):
        try:
            response = requests.get(
                f"https://pokeapi.co/api/v2/pokemon/{self.textbox.text()}", timeout=5
            )

            if response.status_code == 200:
                self.response = response.json()
                self.img_data = requests.get(
                    self.response["sprites"]["other"]["official-artwork"][
                        "front_default"
                    ]
                ).content
            else:
                self.notif.display_notification("The given pokemon could not be found!")
        except requests.Timeout:
            self.notif.display_notification(
                "The Request timed out, please try again later"
            )

    def _show_image(self):
        poke_pic = QPixmap()
        poke_pic.loadFromData(self.img_data)
        self.pokemon_image.setPixmap(poke_pic.scaled(200, 200))

    def _show_stats(self):
        stats = {
            "Name": self.response["name"].title(),
            "Abilities": tuple(
                item["ability"]["name"] for item in self.response["abilities"]
            ),
            "Types": tuple(item["type"]["name"] for item in self.response["types"]),
            "Hp": self.response["stats"][0]["base_stat"],
            "Attack": self.response["stats"][1]["base_stat"],
            "Defense": self.response["stats"][2]["base_stat"],
            "Special-attack": self.response["stats"][3]["base_stat"],
            "Special-defense": self.response["stats"][4]["base_stat"],
            "Speed": self.response["stats"][5]["base_stat"],
        }

        stats_text = ""
        for key in stats:
            if type(stats[key]) == tuple:
                stats_text += key + ": " + ", ".join(stats[key]) + "\n"
            else:
                stats_text += key + ": " + str(stats[key]) + "\n"
        self.stats.setPlainText(stats_text)

    def __init__(self):
        super().__init__()

        self.captured_pokemon = []
        self.notif = Notification()

        self.bg = QLabel(self)
        self.bg.setGeometry(0, 0, 750, 480)
        self.bg_img = QPixmap("assets/bg_2.jpg")
        self.bg.setPixmap(self.bg_img)

        self.setStyleSheet(
            """
            QLineEdit {
                background-color: black;
                font-size: 20px;
                font-weight: 500;
                border: 1px solid gray;
            }
            QPushButton {
                background-color: black;
                font-size: 16px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #fc0303 ;
            }
        """
        )
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.setGeometry(50, 70, 160, 40)
        self.textbox.setStyleSheet("font-size: 16px;")
        self.textbox.returnPressed.connect(self.search)

        label1 = QLabel("Enter the name", self)
        label1.setGeometry(50, 25, 600, 70)

        enter_button = QPushButton("Search", self)
        enter_button.setGeometry(50, 225, 160, 43)
        enter_button.clicked.connect(self.search)

        capture_button = QPushButton("Capture", self)
        capture_button.setGeometry(50, 275, 160, 43)
        capture_button.clicked.connect(self.capture)

        display_button = QPushButton("Display", self)
        display_button.setGeometry(50, 325, 160, 43)
        display_button.clicked.connect(self.display)

        self.pokemon_image = QLabel(parent=self)
        self.pokemon_image.setGeometry(350, 10, 200, 200)

        self.stats = QTextEdit(self)
        self.stats.setGeometry(350, 220, 400, 260)
        self.stats.setFrameStyle(QFrame.NoFrame)
        self.stats.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.stats.setFontPointSize(15)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec())
