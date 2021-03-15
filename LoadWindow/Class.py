# -*- coding: UTF-8 -*-
# editor: JiaYunSong

import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog


def Get_ImagePath():
    return os.path.split(os.path.realpath(__file__))[0].replace('\\', '/') + '/Resources/Foreground.jpg'


class Window(QDialog):
    def __init__(self):

        QDialog.__init__(self)
        self.resize(1016, 488)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 无边框，置顶
        self.setStyleSheet(f"image:url({Get_ImagePath()});")
