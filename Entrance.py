# -*- coding: UTF-8 -*-
# editor: JiaYunSong

import sys
from PyQt5.QtWidgets import QApplication

import LoadWindow.Class
import MainWindow.Class


def main():
    GraphPath = './DataSource/Graph/Graph.csv'
    QueryPath = './DataSource/QueryLog/queryLog.history'
    SightPath = './DataSource/Sightseeing/Sightseeing.csv'
    QtxtPath = './DataSource/FAQsys/Q.txt'
    AtxtPath = './DataSource/FAQsys/A.txt'

    app = QApplication(sys.argv)
    loadWindow = LoadWindow.Class.Window()
    loadWindow.show()
    mainWindow = MainWindow.Class.Window(GraphPath, QueryPath, SightPath, QtxtPath, AtxtPath)
    mainWindow.show()
    loadWindow.close()
    sys.exit(app.exec_())
