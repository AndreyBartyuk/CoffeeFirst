from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from EditFormDesign import Ui_EditWindow
from MainWindowDesign import Ui_MainWindow
import sqlite3
import sys


class EditCoffeeForm(QMainWindow, Ui_EditWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.edits = [self.id, self.sort, self.roast, self.form,
                      self.description, self.price, self.packing]
        self.price.setMinimum(1)
        self.price.setMaximum(999999)
        self.packing.setMinimum(1)
        self.packing.setMaximum(999999)
        self.id.setEnabled(False)
        self.confirm_btn.clicked.connect(self.confirm)

    def show_edit(self):
        self.clear()
        cursor = self.connection.cursor()
        chosen_id = self.parent().id_box.currentText()
        data = cursor.execute(f"SELECT Coffees.id, sort, roasting, hammering, description, price, "
                              f"packing FROM Coffees "
                              f"INNER JOIN Roastings ON Roastings.id = roasting_id "
                              f"INNER JOIN Hammerings ON Hammerings.id = hammering_id "
                              f"WHERE Coffees.id = {chosen_id}").fetchone()
        id_, sort, roast, form, description, price, packing = data
        self.roast.addItems(["Светлая", "Средняя", "Тёмная"])
        self.form.addItems(["В зёрнах", "Молотый"])
        self.id.setText(str(id_))
        self.sort.setText(sort)
        self.roast.setCurrentText(roast)
        self.form.setCurrentText(form)
        self.description.setPlainText(description)
        self.price.setValue(price)
        self.packing.setValue(packing)
        self.show()

    def show_new(self):
        self.clear()
        self.roast.addItems(["Светлая", "Средняя", "Тёмная"])
        self.form.addItems(["В зёрнах", "Молотый"])
        self.price.setValue(1)
        self.packing.setValue(1)
        self.id.setText("-")
        self.show()

    def confirm(self):
        self.status.clearMessage()
        id_ = self.id.text()
        data = (self.sort.text(),
                ["Светлая", "Средняя", "Тёмная"].index(self.roast.currentText()) + 1,
                ["В зёрнах", "Молотый"].index(self.form.currentText()) + 1,
                self.description.toPlainText(), self.price.value(), self.packing.value())
        if not all(data):
            self.status.showMessage("Ошибка! Все поля должны быть заполнены.")
            return None
        cursor = self.connection.cursor()
        if id_ == "-":
            cursor.execute("INSERT INTO Coffees(sort, roasting_id, hammering_id, "
                           "description, price, packing) "
                           "VALUES(?, ?, ?, ?, ?, ?)", data)
            self.connection.commit()
        else:
            cursor.execute("UPDATE Coffees SET sort = ?, roasting_id = ?, hammering_id = ?, "
                           "description = ?, price = ?, packing = ? WHERE id = ?", data + (id_,))
            self.connection.commit()
        self.parent().load_data()
        self.close()

    def clear(self):
        for edit in self.edits:
            edit.clear()


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.edit_form = EditCoffeeForm(self)
        self.edit_btn.clicked.connect(self.edit_form.show_edit)
        self.new_btn.clicked.connect(self.edit_form.show_new)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.load_data()

    def load_data(self):
        cursor = self.connection.cursor()
        data = cursor.execute("SELECT Coffees.id, sort, roasting, hammering, description, price, "
                              "packing FROM Coffees "
                              "INNER JOIN Roastings ON Roastings.id = roasting_id "
                              "INNER JOIN Hammerings ON Hammerings.id = hammering_id").fetchall()
        self.table.clear()
        self.table.setColumnCount(7)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(["ID", "Сорт", "Обжарка", "Форма",
                                              "Описание", "Цена", "Объем"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        for i, row in enumerate(data):
            for j, element in enumerate(row):
                text = str(element)
                if j == 5:
                    text += " ₽"
                elif j == 6:
                    text += " г"
                self.table.setItem(i, j, QTableWidgetItem(text))
        self.id_box.clear()
        self.id_box.addItems([str(x[0]) for x in data])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Coffee()
    window.show()
    sys.exit(app.exec())
