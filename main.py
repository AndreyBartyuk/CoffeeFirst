from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
from PyQt6.QtGui import QPainter, QColor
from PyQt6 import uic
from random import randint
import sys


class YellowCircles(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.setWindowTitle("Желтые окружности")
        self.setFixedSize(self.width(), self.height())
        self.draw_button.clicked.connect(self.draw_circle)
        self.color = QColor("#fefe22")
        self.drawing = False

    def draw_circle(self):
        self.drawing = True
        self.repaint()
        self.drawing = False

    def paintEvent(self, event):
        if self.drawing:
            qp = QPainter(self)
            qp.setBrush(self.color)
            size = randint(10, 200)
            qp.drawEllipse(randint(0, self.width() - size),
                           randint(0, self.height() - size), size, size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YellowCircles()
    window.show()
    sys.exit(app.exec())
