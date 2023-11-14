import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

d_ = {0: "id", 1: "name", 2: "degree", 3: "type", 4: "description", 5: "price", 6: "volume"}


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        self.load_table()

    def load_table(self):
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
        self.tableWidget.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column):
        col = d_[column]
        text = self.tableWidget.item(row, column).text()
        id = int(self.tableWidget.item(row, 0).text())
        query = f"UPDATE coffee SET {col} = '{text}' WHERE id = {id}"
        self.cursor.execute(query)
        self.connection.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())
