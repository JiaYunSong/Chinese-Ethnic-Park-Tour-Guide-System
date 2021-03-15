# -*- coding: UTF-8 -*-
# editor: JiaYunSong

import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

import MainWindow.ChildWindows.SchedulingPage.Ui.window
import MainWindow.ChildWindows.SchedulingPage.Function.IntelligentScheduling as AiScl


def Get_ImagePath():
    return os.path.split(os.path.realpath(__file__))[0].replace('\\', '/') + '/Ui/Resources/Qi.png'


class Window(QtWidgets.QDialog):
    def __init__(self, MesBox):
        """
        :param MesBox: 主窗口信息栏
        """
        self.MesBox = MesBox
        super(Window, self).__init__()
        self.Dialog = MainWindow.ChildWindows.SchedulingPage.Ui.window.Ui_Dialog()
        self.Dialog.setupUi(self)
        self.Dialog.widget.setPixmap(QtGui.QPixmap(Get_ImagePath()))
        self.Dialog.Search_Button.clicked.connect(self.Mix)

    def Show(self):
        self.show()

    def Mix(self):
        try:
            ticketPrice = int(self.Dialog.Input01_TextEdit.toPlainText())
            flowVolume = int(self.Dialog.Input02_TextEdit.toPlainText())
            guidancePrice = int(self.Dialog.Input05_TextEdit.toPlainText())
            maxGuidanceNum = int(self.Dialog.Input06_TextEdit.toPlainText())
            tolerance = int(self.Dialog.Input03_TextEdit.toPlainText())
            serviceTime = int(self.Dialog.Input04_TextEdit.toPlainText())
            profit,Num = AiScl.optimize(ticketPrice,flowVolume,guidancePrice,maxGuidanceNum,tolerance,serviceTime)
            self.Dialog.Output_Label_1.setText(str(int(Num)))
            self.Dialog.Output_Label_2.setText(str(int(profit*100)/100))
        except Exception as e:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '输入有误或模型不支持，请检查输入框！', QMessageBox.Yes)
            self.MesBox.setPlainText(f"Message：{e}.")
