from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QTableView, QTableWidgetItem, QItemDelegate
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QImage, QPixmap
from PyQt5.QtCore import QSortFilterProxyModel
import sys
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import urllib.request
import webbrowser




class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        return super(PandasModel, self).headerData(section, orientation, role)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if not index.isValid():
            return QtCore.QVariant()
        if index.row() == 0:
            return QtCore.QVariant(self._df.columns.values[index.column()])
        return QtCore.QVariant(str(self._df.iloc[index.row()-1, index.column()]))

    def setData(self, index, value, role):
        if index.row() == 0:
            if isinstance(value, QtCore.QVariant):
                value = value.value()
            if hasattr(value, 'toPyObject'):
                value = value.toPyObject()
            self._df.columns.values[index.column()] = value
            self.headerDataChanged.emit(QtCore.Qt.Horizontal, index.column(), index.column())
        else:
            col = self._df.columns[index.column()]
            row = self._df.index[index.row()]
            if isinstance(value, QtCore.QVariant):
                value = value.value()
            if hasattr(value, 'toPyObject'):
                value = value.toPyObject()
            else:
                dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
                self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)+1 

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)


class Info(QMainWindow):
	def __init__(self):
		super().__init__()
		self.w = None
		self.info = uic.loadUi('info.ui', self)
		self.setFixedSize(720, 420)

	def display(self):
		self.show()

class About(QMainWindow):
	def __init__(self):
		super().__init__()
		self.w = None
		self.about = uic.loadUi('about.ui', self)
		self.setFixedSize(400, 250)

		self.pushButton.clicked.connect(self.facebook)
		self.pushButton_2.clicked.connect(self.github)
		self.pushButton_3.clicked.connect(self.gmail)

	def facebook(self):
		webbrowser.open("https://www.facebook.com/huynhvan.thinh.399", new=2)

	def github(self):
		webbrowser.open("https://github.com/huynhvanthinh28", new=2)

	def gmail(self):
		webbrowser.open("https://mail.google.com/mail/u/0/?ogbl#inbox", new=2)

	def display(self):
		self.show()

class Data(QMainWindow):
	def __init__(self, data):
		super().__init__()
		self.w = None
		self.data = uic.loadUi('data.ui', self)
		self.setFixedSize(1280, 720)

		self.model = QStandardItemModel(len(data.axes[1]), len(data.axes[0]))
		self.model.setHorizontalHeaderLabels(data.columns)
		self.stat_df = data.sort_index()
		self.model = PandasModel(data)
		self.tableView.setModel(self.model)
		for i in range(self.model.columnCount()):
			ix = self.model.index(-1, i)
			self.tableView.openPersistentEditor(ix)
		stylesheet = "::section{Background-color:rgb(192,192,192);}"
		self.tableView.verticalHeader().setStyleSheet(stylesheet)
		self.tableView.horizontalHeader().setStyleSheet(stylesheet)

	def display(self):
		self.show()

class Whiskey(QtWidgets.QMainWindow):
	def __init__(self):
		super(Whiskey, self).__init__()
		self.ui = uic.loadUi('whiskey.ui', self)
		self.df = pd.read_excel('Whisky_Data.xlsx')
		self.df.drop('Unnamed: 0', axis=1, inplace=True)
		self.setFixedSize(1280,720)
		print(self.df['price'][0])
		print(self.df['Link'][0])
		self.label_2.setText(self.df['price'][0])
		self.label_6.setText(self.df['name'][0])
		self.label_7.setText('0')

		self.img = self.df['Link'][0]

		self.image = QImage()
		self.image.loadFromData(requests.get(self.img).content)

		pixmap5 = self.image.scaled(285, 350)
		scene = QtWidgets.QGraphicsScene(self)
		pixmap = QPixmap(pixmap5)
		item = QtWidgets.QGraphicsPixmapItem(pixmap)
		scene.addItem(item)
		self.ui.graphicsView.setScene(scene)
		self.pushButton.clicked.connect(self.Info)
		self.pushButton_4.clicked.connect(self.About)
		self.pushButton_2.clicked.connect(self.Data)
		self.pushButton_3.clicked.connect(self.web)
		self.pushButton_8.clicked.connect(self.choose)
		self.pushButton_10.clicked.connect(self.op)


		self.data = Data(self.df)

		self.info = Info()

		self.about = About()


	def Data (self):
		self.data.display()

	def Info(self):
		self.info.display()

	def About(self):
		self.about.display()


	def choose(self):
		i =random.randint(0, 103)
		self.label_2.setText(self.df['price'][i])

		self.img = self.df['Link'][i]

		self.image = QImage()
		self.image.loadFromData(requests.get(self.img).content)

		pixmap5 = self.image.scaled(285, 350)
		scene = QtWidgets.QGraphicsScene(self)
		pixmap = QPixmap(pixmap5)
		item = QtWidgets.QGraphicsPixmapItem(pixmap)
		scene.addItem(item)
		self.ui.graphicsView.setScene(scene)

		self.label_6.setText(self.df['name'][i])
		self.label_7.setText(str(i))

	def op(self):
		a = self.lineEdit.text()
		print(type(a))
		try:
			if a !='':
				self.label_2.setText(self.df['price'][int(a)])
				self.img = self.df['Link'][int(a)]

				self.image = QImage()
				self.image.loadFromData(requests.get(self.img).content)

				pixmap5 = self.image.scaled(285, 350)
				scene = QtWidgets.QGraphicsScene(self)
				pixmap = QPixmap(pixmap5)
				item = QtWidgets.QGraphicsPixmapItem(pixmap)
				scene.addItem(item)
				self.ui.graphicsView.setScene(scene)

				self.label_6.setText(self.df['name'][int(a)])
				self.label_7.setText(str(int(a)))

		except:
			print('oh oh')

	def web(self):
		webbrowser.open("https://www.thewhiskyexchange.com/c/35/japanese-whisky", new=1)


app = QApplication(sys.argv)
window = Whiskey()
window.show()
app.exec()