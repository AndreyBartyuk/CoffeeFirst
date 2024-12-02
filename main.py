from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
from PyQt6.QtGui import QPainter, QColor
from random import randint
import sys


class RandomCircles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Случайные окружности")
        self.setFixedSize(600, 500)

        self.draw_button = QPushButton("Случайная окружность", self)
        self.draw_button.setGeometry(10, 450, 580, 40)
        self.draw_button.clicked.connect(self.draw_circle)

        self.drawing = False

    def draw_circle(self):
        self.drawing = True
        self.repaint()
        self.drawing = False

    def paintEvent(self, event):
        if self.drawing:
            qp = QPainter(self)
            color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
            qp.setBrush(color)
            size = randint(10, 200)
            qp.drawEllipse(randint(0, self.width() - size),
                           randint(0, self.height() - size), size, size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomCircles()
    window.show()
    sys.exit(app.exec())
