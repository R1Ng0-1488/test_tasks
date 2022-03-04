from django.core.management.base import BaseCommand
from PyQt5 import QtCore, QtGui, QtWidgets

import time 
import requests


CHOICES = {
    'Разворот строки.': 'string_reverse',
    'Перестановку четных и нечетных символов.': 'string_double_reverse',
    'Повтор символа в строке согласно его позиции.': 'string_position_repeat'
}


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, SecondWindow):
        self.SecondWindow = SecondWindow
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(220, 50, 300, 191))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 90, 300, 31))
        self.textEdit.setObjectName("Получить айди задачи")
        
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(50, 140, 171, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.get_request)
        
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(0, 40, 300, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(CHOICES.keys())
        
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(100, 0, 101, 21))
        self.label.text = "label"
        
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(80, 280, 231, 201))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(60, 0, 100, 16))
        self.label_2.setObjectName("label_2")
        
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 50, 231, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 130, 191, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.get_status)
        
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(430, 280, 231, 201))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(60, 0, 130, 16))
        self.label_3.setObjectName("label_3")
        
        self.textEdit_3 = QtWidgets.QTextEdit(self.frame_3)
        self.textEdit_3.setGeometry(QtCore.QRect(0, 50, 231, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 130, 191, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.get_result)

        self.MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")

        self.menutwo = QtWidgets.QAction('Пакетный режим')
        self.menutwo.setObjectName("menutwo")
        
        self.MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        self.MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menutwo)
        self.menutwo.triggered.connect(self.one_action)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "Создать задачу"))
        self.label_2.setText(_translate("MainWindow", "Получить статус"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label_3.setText(_translate("MainWindow", "Получить результат"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))

    def get_request(self):
    
        data = {
            'task_type': CHOICES[self.comboBox.currentText()],
            'data': self.textEdit.toPlainText() 
        }
        
        res = requests.post('http://localhost:8000', data=data)
        data = res.json()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(f'Айди вашей задачи')
        if data.get('Result'):
            message.setText(f"{data.get('task_id')}")
            textEdit = QtWidgets.QTextEdit(message)
            textEdit.setGeometry(QtCore.QRect(11, 10, 300, 31))
            textEdit.setObjectName("Получить айди задачи")
            textEdit.setPlainText(f"{data.get('task_id')}")
        else:
            message.setText(f"{' '.join(*data.get('errors').values())}")
        message.exec_()

    def get_status(self):
        data = {
            'task_id': self.textEdit_2.toPlainText() 
        }
        res = requests.post('http://localhost:8000/get_status/', data=data)
        data = res.json()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(f'Получить статус')
        if data.get('Result'):
            message.setText(f"{data.get('task_status')}")
        else:
            message.setText(f"{' '.join(*data.get('errors').values())}")
        message.exec_()

    def get_result(self):
        data = {
            'task_id': self.textEdit_2.toPlainText() 
        }
        res = requests.post('http://localhost:8000/get_result/', data=data)
        data = res.json()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(f'Получить статус')

        if data.get('Result'):
            message.setText(f"{data.get('task_result')}")
        else:
            message.setText(f"{' '.join(*data.get('errors').values())}")
        message.exec_()

    def one_action(self):
        self.MainWindow.close()
        self.SecondWindow.show()


class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.MainWindow = MainWindow
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(220, 50, 300, 191))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 90, 300, 31))
        self.textEdit.setObjectName("Получить айди задачи")
        
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(50, 140, 171, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.get_request)
        
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(0, 40, 300, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(CHOICES.keys())
        
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(100, 0, 101, 21))
        self.label.text = "label"

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        self.menuOne = QtWidgets.QAction('Обычный режим')
        self.menuOne.setObjectName("menuOne")

        self.menubar.addAction(self.menuOne)
        self.menuOne.triggered.connect(self.one_action)


        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "Создать задачу"))
 
    def one_action(self):
        self.MainWindow.show()
        self.close()

    def loop(self, task_id, message):
        def get_status(task_id):
            data = {
                'task_id': task_id
            }
            res = requests.post('http://localhost:8000/get_status/', data=data)
            data = res.json()
            return data.get('task_status')

        def get_result(task_id):
            data = {
                'task_id': task_id
            }
            res = requests.post('http://localhost:8000/get_result/', data=data)
            data = res.json()
            return data.get('task_result')

        while True:
            r = get_status(task_id)
            if r == 'SUCCESS':
                message.done(1)
                message.setText(get_result(task_id))
                break
            time.sleep(1)

    def get_request(self):
    
        data = {
            'task_type': CHOICES[self.comboBox.currentText()],
            'data': self.textEdit.toPlainText() 
        }
        
        res = requests.post('http://localhost:8000', data=data)
        data = res.json()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(f'Айди вашей задачи')
        if data.get('Result'):
            self.loop(data.get('task_id'), message)
        else:
            message.setText(f"{' '.join(*data.get('errors').values())}")
        message.exec_()



    


class Command(BaseCommand):
    help = "Create pyqt"

    def handle(self, *args, **options):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow, SecondWindow(MainWindow))
        MainWindow.show()
        sys.exit(app.exec_())