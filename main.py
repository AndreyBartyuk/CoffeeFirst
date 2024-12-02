from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic
import sqlite3
import sys


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.connection = sqlite3.connect("coffee.sqlite")
        self.load_table()

    def load_table(self):
        cursor = self.connection.cursor()
        data = cursor.execute("SELECT Coffees.id, sort, roasting, hammering, description, price, "
                              "packing FROM Coffees "
                              "INNER JOIN Roastings ON Roastings.id = roasting_id "
                              "INNER JOIN Hammerings ON Hammerings.id = hammering_id").fetchall()
        self.table.setColumnCount(7)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(["ID", "Сорт", "Обжарка", "Форма",
                                              "Описание", "Цена", "Объем"])
        for i, row in enumerate(data):
            for j, element in enumerate(row):
                text = str(element)
                if j == 5:
                    text += " ₽"
                elif j == 6:
                    text += " г"
                self.table.setItem(i, j, QTableWidgetItem(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Coffee()
    window.show()
    sys.exit(app.exec())
