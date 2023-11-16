import sys
import sqlite3
from main_design import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow2
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

d_ = {0: "id", 1: "name", 2: "degree", 3: "type", 4: "description", 5: "price", 6: "volume"}


class Espresso(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        self.tableWidget.cellChanged.connect(self.cell_changed)
        self.addButton.clicked.connect(self.adding)
        self.load_table()

    def load_table(self):
        self.tableWidget.clear()
        data = self.cursor.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Степень обжарки', 'Молотый/в зернах', 'Описание', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()

    def cell_changed(self, row, column):
        col = d_[column]
        text = self.tableWidget.item(row, column).text()
        id = int(self.tableWidget.item(row, 0).text())
        query = f"UPDATE coffee SET {col} = '{text}' WHERE id = {id}"
        self.cursor.execute(query)
        self.connection.commit()

    def adding(self):
        self.widget = AddWidget(self)
        self.widget.show()


class AddWidget(QMainWindow, Ui_MainWindow2):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        self.addButtonFromForm.clicked.connect(self.add_from_form)

    def add_from_form(self):
        id = int(self.id_input.text())
        name = self.name_input.text()
        degree = self.degree_input.text()
        type = self.type_input.text()
        description = self.description_input.text()
        price = self.price_input.text()
        volume = self.volume_input.text()
        query = "INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (id, name, degree, type, description, price, volume))
        self.connection.commit()
        self.parent().load_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())
