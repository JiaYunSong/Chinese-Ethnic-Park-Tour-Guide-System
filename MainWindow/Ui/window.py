# -*- coding: utf-8 -*-
# editor: JiaYunSong
# Created by: PyQt5 UI code generator 5.15.0

import os
from PyQt5 import QtCore, QtGui, QtWidgets


def Get_ImagePath():
    return os.path.split(os.path.realpath(__file__))[0].replace('\\', '/') + '/Resources/Background.jpg'


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("MDialog")
        Dialog.resize(1441, 861)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        Dialog.setStyleSheet('#MDialog{'+f"image:url({Get_ImagePath()});"+'}')
        self.WTitle_widget = QtWidgets.QWidget(Dialog)
        self.WTitle_widget.setGeometry(QtCore.QRect(0, 0, 1361, 31))
        self.WTitle_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.WTitle_widget.setObjectName("WTitle_widget")
        self.Mes_plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.Mes_plainTextEdit.setGeometry(QtCore.QRect(150, 820, 1281, 31))
        self.Mes_plainTextEdit.setStyleSheet("background-color: rgba(0, 0, 0, 120);\n"
            "color: rgb(255, 255, 255);")
        self.Mes_plainTextEdit.setObjectName("Mes_plainTextEdit")
        self.Mudole_widget = QtWidgets.QWidget(Dialog)
        self.Mudole_widget.setGeometry(QtCore.QRect(0, 30, 141, 241))
        self.Mudole_widget.setObjectName("Mudole_widget")

        buttomStyle = "QPushButton {background-color : #00000000;} " \
                      "QPushButton:hover{background-color: #33FFFFFF;}" \
                      "QPushButton:pressed {background-color: #00000000;}"
        self.PathGuide_Button = QtWidgets.QPushButton(self.Mudole_widget)
        self.PathGuide_Button.setGeometry(QtCore.QRect(0, 0, 141, 61))
        self.PathGuide_Button.setStyleSheet(buttomStyle)
        self.PathGuide_Button.setText("")
        self.PathGuide_Button.setObjectName("PathGuide_Button")
        self.Mange_Button = QtWidgets.QPushButton(self.Mudole_widget)
        self.Mange_Button.setGeometry(QtCore.QRect(0, 180, 141, 61))
        self.Mange_Button.setStyleSheet(buttomStyle)
        self.Mange_Button.setText("")
        self.Mange_Button.setObjectName("Mange_Button")
        self.QA_Button = QtWidgets.QPushButton(self.Mudole_widget)
        self.QA_Button.setGeometry(QtCore.QRect(0, 60, 141, 61))
        self.QA_Button.setStyleSheet(buttomStyle)
        self.QA_Button.setText("")
        self.QA_Button.setObjectName("QA_Button")
        self.Optimize_Button = QtWidgets.QPushButton(self.Mudole_widget)
        self.Optimize_Button.setGeometry(QtCore.QRect(0, 120, 141, 61))
        self.Optimize_Button.setStyleSheet(buttomStyle)
        self.Optimize_Button.setText("")
        self.Optimize_Button.setObjectName("Optimize_Button")
        self.WMini_Button = QtWidgets.QPushButton(Dialog)
        self.WMini_Button.setGeometry(QtCore.QRect(1360, 0, 41, 31))
        self.WMini_Button.setStyleSheet(buttomStyle)
        self.WMini_Button.setText("")
        self.WMini_Button.setObjectName("WMini_Button")
        self.WClose_Button = QtWidgets.QPushButton(Dialog)
        self.WClose_Button.setGeometry(QtCore.QRect(1400, 0, 41, 31))
        self.WClose_Button.setStyleSheet(buttomStyle)
        self.WClose_Button.setText("")
        self.WClose_Button.setObjectName("WClose_Button")
        self.Module_stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.Module_stackedWidget.setGeometry(QtCore.QRect(140, 30, 1301, 781))
        self.Module_stackedWidget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.Module_stackedWidget.setObjectName("Module_stackedWidget")

        self.retranslateUi(Dialog)
        self.WClose_Button.clicked.connect(Dialog.close)
        self.WMini_Button.clicked.connect(Dialog.showMinimized)
        self.WClose_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.WMini_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PathGuide_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Mange_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.QA_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        def mousePressEvent(*args):
            if args[0].button() == QtCore.Qt.LeftButton:
                Dialog.m_flag = True
                Dialog.m_Position = args[0].globalPos() - Dialog.pos()  # 获取鼠标相对窗口的位置
                args[0].accept()
                Dialog.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))  # 更改鼠标图标
        self.WTitle_widget.mousePressEvent = mousePressEvent

        def mouseMoveEvent(*args):
            if QtCore.Qt.LeftButton and Dialog.m_flag:
                Dialog.move(args[0].globalPos() - Dialog.m_Position)  # 更改窗口位置
                args[0].accept()
        self.WTitle_widget.mouseMoveEvent = mouseMoveEvent

        def mouseReleaseEvent(*args):
            Dialog.m_flag = False
            Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.WTitle_widget.mouseReleaseEvent = mouseReleaseEvent

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Mes_plainTextEdit.setPlainText(_translate("Dialog", "Message：None..."))
