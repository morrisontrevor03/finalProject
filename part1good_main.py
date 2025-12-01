import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from part1good import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.characterSlider.valueChanged.connect(self.on_slider_changed)

        # initialize label and generate button
        self.characterLabel.setText(f"# of Characters: {self.characterSlider.value()}")
        self.generateButton.clicked.connect(self.generateButtonPressed)
    
    def generateButtonPressed(self):
        self.handle_enter()

    def on_slider_changed(self, value):
        self.characterLabel.setText(f"# of Characters: {value}")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.handle_enter()

    def handle_enter(self):
        self.resultLabel.setText(f"Your New Password: {self.generate_password(int(self.characterSlider.value()))}")

    def generate_password(self, length):
        password = ""
        for i in range(length):
            password += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:,.<>?/~')
        return password


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())