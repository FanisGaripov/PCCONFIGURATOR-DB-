import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget, QComboBox, QMessageBox


class PCconf(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('PC_Configurator.ui', self)  # Загружаем дизайн
        self.setWindowTitle("Конфигуратор ПК")  # задаем заголовок
        self.move(500, 100)  # перемещаем по экрану
        self.init_UI()

    def init_UI(self):
        # добавляем реакцию на нажатие кнопок
        self.pushButton.clicked.connect(self.updateTable)
        self.pushButton_4.clicked.connect(self.calc_sum)
        self.pushButton_2.clicked.connect(self.otc)
        self.pushButton_5.clicked.connect(self.spravka)
        self.pushButton_6.clicked.connect(self.dobavka2)
        self.pushButton_7.clicked.connect(self.dobavka3)
        self.pushButton_8.clicked.connect(self.dobavka4)
        self.pushButton_9.clicked.connect(self.dobavka5)
        self.pushButton_3.clicked.connect(self.reload_window)

        # создание combobox'ов для дальнейшего их заполнения
        self.combo_box1 = QComboBox(self)
        self.combo_box1.setGeometry(20, 20, 161, 22)
        self.combo_box2 = QComboBox(self)
        self.combo_box2.setGeometry(20, 50, 161, 22)
        self.combo_box3 = QComboBox(self)
        self.combo_box3.setGeometry(20, 80, 161, 22)
        self.combo_box4 = QComboBox(self)
        self.combo_box4.setGeometry(20, 110, 161, 22)
        self.combo_box5 = QComboBox(self)
        self.combo_box5.setGeometry(20, 140, 161, 22)

        # подключаем базу данных
        self.con = sqlite3.connect('daba.db')
        self.cur = self.con.cursor()

        # считываем данные из БД
        res1 = self.cur.execute('''SELECT * FROM comp''').fetchall()

        # обновляем каждый комбобокс и добвляем в него данные из таблицы
        # 1 комбобокс
        self.cur.execute("SELECT Name From Names")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box1.addItem(row[0])
        # 2 комбобокс
        self.cur.execute("SELECT Models FROM Processors")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box2.addItem(row[0])
        # 3 комбобокс
        self.cur.execute("SELECT Models FROM Videocards")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box3.addItem(row[0])
        # 4 комбобокс
        self.cur.execute("SELECT Models FROM Operativka")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box4.addItem(row[0])
        # 5 комбобокс
        self.cur.execute("SELECT Models FROM Pamyat")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box5.addItem(row[0])

        # выводим на экран значения
        self.tableWidget.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def get_price1(self):
        # функция для получения цены процессора
        self.Models = self.combo_box2.currentText()
        self.cur.execute("SELECT Stoimost FROM Processors WHERE Models=?", (self.Models,))
        price = self.cur.fetchone()
        if price:
            self.lineEdit_2.setText(str(price[0]))
        else:
            self.lineEdit_2.setText("Price not available")

    def get_price2(self):
        # функция для получения цены видеокарты
        self.Models = self.combo_box3.currentText()
        self.cur.execute("SELECT Stoimost FROM Videocards WHERE Models=?", (self.Models,))
        price = self.cur.fetchone()
        if price:
            self.lineEdit_3.setText(str(price[0]))
        else:
            self.lineEdit_3.setText("Price not available")

    def get_price3(self):
        # функция для получения цены оперативной памяти
        self.Models = self.combo_box4.currentText()
        self.cur.execute("SELECT Stoimost FROM Operativka WHERE Models=?", (self.Models,))
        price = self.cur.fetchone()
        if price:
            self.lineEdit_4.setText(str(price[0]))
        else:
            self.lineEdit_4.setText("Price not available")

    def get_price4(self):
        # функция для получения цены накопителей
        self.Models = self.combo_box5.currentText()
        self.cur.execute("SELECT Stoimost FROM Pamyat WHERE Models=?", (self.Models,))
        price = self.cur.fetchone()
        if price:
            self.lineEdit_5.setText(str(price[0]))
        else:
            self.lineEdit_5.setText("Price not available")

    def updateTable(self, index):
        # Получить данные из QComboBox
        # присваиваем значение переменным с комбобоксов
        self.id = self.combo_box1.currentText()
        self.fam = self.combo_box2.currentText()
        self.nam = self.combo_box3.currentText()
        self.otch = self.combo_box4.currentText()
        self.kurs = self.combo_box5.currentText()
        self.cur = self.con.cursor()
        self.summa = self.lineEdit.text()

        self.combo_box2.currentIndexChanged.connect(self.get_price1)
        self.combo_box3.currentIndexChanged.connect(self.get_price2)
        self.combo_box4.currentIndexChanged.connect(self.get_price3)
        self.combo_box5.currentIndexChanged.connect(self.get_price4)

        # Добавляем данные в таблицу
        if self.id != '' and self.fam != '' and self.nam != '' and self.otch != '' and self.kurs != '' and self.summa != 0:
            self.cur.execute("""INSERT INTO comp VALUES (?, ?, ?, ?, ?, ?)""",
                             (self.id, self.fam, self.nam, self.otch, self.kurs, self.summa))
        res1 = self.cur.execute('''SELECT * FROM comp''').fetchall()

        # Отображаем данные в таблице
        self.tableWidget.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()

    def otc(self):
        # присваиваем значение переменным с комбобоксов
        self.id = self.combo_box1.currentText()
        self.fam = self.combo_box2.currentText()
        self.nam = self.combo_box3.currentText()
        self.otch = self.combo_box4.currentText()
        self.kurs = self.combo_box5.currentText()
        self.cur = self.con.cursor()

        self.combo_box2.currentIndexChanged.connect(self.get_price1)
        self.combo_box3.currentIndexChanged.connect(self.get_price2)
        self.combo_box4.currentIndexChanged.connect(self.get_price3)
        self.combo_box5.currentIndexChanged.connect(self.get_price4)

        # удаляем данные из базы данных
        if self.id != '' and self.nam != '' and self.fam != '':
            self.cur.execute("""DELETE FROM comp WHERE id = ? and nam = ? and fam = ? and otch = ? and kurs = ?""",
                             (self.id, self.nam, self.fam, self.otch, self.kurs))
        res1 = self.cur.execute('''SELECT * FROM comp''').fetchall()

        # отображаем изменения в таблице
        self.tableWidget.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()

    def dobavka2(self):
        # Отображение окна добавления процессоров
        self.d2 = Dobavit2()
        self.d2.show()

    def dobavka3(self):
        # Отображение окна добавления видеокарт
        self.d3 = Dobavit3()
        self.d3.show()

    def dobavka4(self):
        # Отображение окна добавления оперативной памяти
        self.d4 = Dobavit4()
        self.d4.show()

    def dobavka5(self):
        # Отображение окна добавления накопителей
        self.d5 = Dobavit5()
        self.d5.show()

    def spravka(self):
        # Отображение окна "Справка" с инструкцией о том, как пользоваться программой
        self.w1 = Window1()
        self.w1.show()

    def reload_window(self):
        # Функция для обновления данных в комбобоксах после добавления новых комплектующих
        self.combo_box1.clear()
        self.combo_box2.clear()
        self.combo_box3.clear()
        self.combo_box4.clear()
        self.combo_box5.clear()

        # обновляем каждый комбобокс и добвляем в него данные из таблицы
        # 1 комбобокс
        self.cur.execute("SELECT Name From Names")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box1.addItem(row[0])
        # 2 комбобокс
        self.cur.execute("SELECT Models FROM Processors")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box2.addItem(row[0])
        # 3 комбобокс
        self.cur.execute("SELECT Models FROM Videocards")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box3.addItem(row[0])
        # 4 комбобокс
        self.cur.execute("SELECT Models FROM Operativka")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box4.addItem(row[0])
        # 5 комбобокс
        self.cur.execute("SELECT Models FROM Pamyat")
        data = self.cur.fetchall()
        for row in data:
            self.combo_box5.addItem(row[0])

    def calc_sum(self):
        try:
            price1 = int(self.lineEdit_2.text())
            price2 = int(self.lineEdit_3.text())
            price3 = int(self.lineEdit_4.text())
            price4 = int(self.lineEdit_5.text())
            summa = price1 + price2 + price3 + price4
            if summa != 0:
                self.lineEdit.setText(str(summa))
        except:
            self.lineEdit.setText("Price not available")


class Dobavit2(QWidget):
    # добавление процессора
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('Dobavka2.ui', self)
        self.setWindowTitle("Добавить процессор")
        self.move(200, 200)
        self.con = None
        self.cur = None
        self.init_UI()

    def init_UI(self):
        self.pushButton.clicked.connect(self.dobavlenie2)
        self.con = sqlite3.connect('daba.db')  # подключаем базу данных
        self.cur = self.con.cursor()
        res2 = self.cur.execute('''SELECT * FROM Processors''').fetchall()

    def closeEvent(self, event):
        self.con.close()
        event.accept()

    def dobavlenie2(self):
        self.Models = self.lineEdit.text()
        self.Stoimost = self.lineEdit_2.text()
        if self.Models != '' and self.Stoimost != '':
            self.cur.execute("""INSERT INTO Processors VALUES (?, ?)""",
                             (self.Models, self.Stoimost))
            res2 = self.cur.execute('''SELECT * FROM Processors''').fetchall()

        self.tableWidget.setRowCount(len(res2))
        for i, elem in enumerate(res2):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()


class Dobavit3(QWidget):
    # добавление видеокарты
    def __init__(self):
        super().__init__()
        uic.loadUi('Dobavka3.ui', self)
        self.setWindowTitle("Добавить видеокарту")
        self.move(200, 200)
        self.con = None
        self.cur = None
        self.init_UI()

    def init_UI(self):
        self.pushButton.clicked.connect(self.dobavlenie3)
        self.con = sqlite3.connect('daba.db')  # подключаем базу данных
        self.cur = self.con.cursor()
        res3 = self.cur.execute('''SELECT * FROM Videocards''').fetchall()

    def closeEvent(self, event):
        self.con.close()
        event.accept()

    def dobavlenie3(self):
        self.Models = self.lineEdit.text()
        self.Stoimost = self.lineEdit_2.text()
        if self.Models != '' and self.Stoimost != '':
            self.cur.execute("""INSERT INTO Videocards VALUES (?, ?)""",
                             (self.Models, self.Stoimost))
            res3 = self.cur.execute('''SELECT * FROM Videocards''').fetchall()

        self.tableWidget.setRowCount(len(res3))
        for i, elem in enumerate(res3):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()


class Dobavit4(QWidget):
    # добавление оперативной памяти
    def __init__(self):
        super().__init__()
        uic.loadUi('Dobavka4.ui', self)
        self.setWindowTitle("Добавить оперативную память")
        self.move(200, 200)
        self.con = None
        self.cur = None
        self.init_UI()

    def init_UI(self):
        self.pushButton.clicked.connect(self.dobavlenie4)
        self.con = sqlite3.connect('daba.db')  # подключаем базу данных
        self.cur = self.con.cursor()
        res4 = self.cur.execute('''SELECT * FROM Operativka''').fetchall()

    def closeEvent(self, event):
        self.con.close()
        event.accept()

    def dobavlenie4(self):
        self.Models = self.lineEdit.text()
        self.Stoimost = self.lineEdit_2.text()
        if self.Models != '' and self.Stoimost != '':
            self.cur.execute("""INSERT INTO Operativka VALUES (?, ?)""",
                             (self.Models, self.Stoimost))
            res4 = self.cur.execute('''SELECT * FROM Operativka''').fetchall()

        self.tableWidget.setRowCount(len(res4))
        for i, elem in enumerate(res4):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()


class Dobavit5(QWidget):
    # добавление накопителей
    def __init__(self):
        super().__init__()
        uic.loadUi('Dobavka5.ui', self)
        self.setWindowTitle("Добавить накопитель")
        self.move(200, 200)
        self.con = None
        self.cur = None
        self.init_UI()

    def init_UI(self):
        self.pushButton.clicked.connect(self.dobavlenie5)
        self.con = sqlite3.connect('daba.db')  # подключаем базу данных
        self.cur = self.con.cursor()
        res5 = self.cur.execute('''SELECT * FROM Pamyat''').fetchall()

    def closeEvent(self, event):
        self.con.close()
        event.accept()

    def dobavlenie5(self):
        self.Models = self.lineEdit.text()
        self.Stoimost = self.lineEdit_2.text()
        if self.Models != '' and self.Stoimost != '':
            self.cur.execute("""INSERT INTO Pamyat VALUES (?, ?)""",
                             (self.Models, self.Stoimost))
            res5 = self.cur.execute('''SELECT * FROM Pamyat''').fetchall()

        self.tableWidget.setRowCount(len(res5))
        for i, elem in enumerate(res5):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()


class Window1(QWidget):
    # справка
    def __init__(self):
        super().__init__()
        uic.loadUi('spravkaSDB.ui', self)
        self.setWindowTitle("Справка")
        self.move(50, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PCconf()
    ex.show()
    sys.exit(app.exec_())