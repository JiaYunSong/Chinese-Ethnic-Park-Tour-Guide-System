# -*- coding: utf-8 -*-
# editor: Su HanYu,JiaYunSong modified from https://github.com/ShaShiDiZhuanLan/Demo_MessageChat_Qt

from PyQt5 import QtWidgets
from PyQt5.QtCore import *

from MainWindow.ChildWindows.RobotWindow.Ui.chat_message import ChatMessage
import MainWindow.ChildWindows.RobotWindow.Ui.window


class Window(QtWidgets.QDialog):
    def __init__(self, FAQRobot, MesBox):
        """
        :param FAQRobot: 主窗口问答机器人
        :param MesBox: 主窗口信息栏
        """
        self.robot = FAQRobot
        self.MesBox = MesBox
        super(Window, self).__init__()
        self.Dialog = MainWindow.ChildWindows.RobotWindow.Ui.window.Ui_Dialog()
        self.Dialog.setupUi(self)
        self.answer("您好，我是人工智能小萱！")
        self.answer("输入您的问题，我将会尽我所能为您回答。")

    def Show(self):
        self.show()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        msg = self.Dialog.textEdit.toPlainText()
        self.Dialog.textEdit.setText('')
        self.ask(msg)
        self.Dialog.listWidget.scrollToBottom()

    def deal_message(self, message: ChatMessage, item: QtWidgets.QListWidgetItem, msg, side):
        message.setFixedWidth(self.width())
        message.msg = msg
        size = message.rect_cons(side)
        item.setSizeHint(size)
        self.Dialog.listWidget.setItemWidget(item, message)

    def answer(self, ans):
        message = ChatMessage(self.Dialog.listWidget.parentWidget())
        item = QtWidgets.QListWidgetItem(self.Dialog.listWidget)
        self.deal_message(message, item, ans, 'left')

    def ask(self, msg):
        message = ChatMessage(self.Dialog.listWidget.parentWidget())
        item = QtWidgets.QListWidgetItem(self.Dialog.listWidget)
        self.deal_message(message, item, msg, 'right')

        # TODO: 回复
        Answer = self.robot.FAQAnswer(msg)
        self.answer(Answer)
