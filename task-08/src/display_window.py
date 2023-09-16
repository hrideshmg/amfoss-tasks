from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot


class DisplayWindow(QWidget):
    @Slot()
    def change_page(self, index):
        if index >= 0 and index <= len(self.captured_pokemon) - 1:  # index starts at 0
            self.name.clear()
            self.artwork.clear()
            # Each element in captured_pokemon is a tuple with the name and image data as the tuple elements
            self.img_pix.loadFromData(self.captured_pokemon[index][1])
            self.artwork.setPixmap(self.img_pix.scaled(400, 400))

            self.name.setText(self.captured_pokemon[index][0])
            self.current_page = index

    def __init__(self, captured_pokemon):
        super().__init__()

        self.captured_pokemon = captured_pokemon
        self.current_page = 0

        self.setFixedSize(512, 512)
        self.setStyleSheet(
            """
            QWidget {
                background-color: black;
            }   
            QPushButton {
                background-color: #1a1a1a;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #fc0303;
            }
        """
        )
        self.artwork = QLabel(parent=self)
        self.artwork.setGeometry(50, 30, 400, 400)
        self.img_pix = QPixmap()

        self.name = QLabel(parent=self)
        self.name.setGeometry(50, 415, 150, 50)
        self.name.setStyleSheet("font-size: 20px;")

        self.prev_button = QPushButton("Previous", self)
        self.prev_button.setGeometry(40, 465, 200, 35)
        self.prev_button.clicked.connect(
            lambda _: self.change_page(self.current_page - 1)
        )
        self.next_button = QPushButton("Next", self)
        self.next_button.setGeometry(270, 465, 200, 35)
        self.next_button.clicked.connect(
            lambda _: self.change_page(self.current_page + 1)
        )

        # Loads the first page by default
        self.change_page(0)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import requests

    app = QApplication([])
    data1 = requests.get(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png"
    ).content
    data2 = requests.get(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
    ).content
    window = DisplayWindow([("Ditto", data1), ("pikachu", data2)])
    window.show()
    app.exec()
