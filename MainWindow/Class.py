# -*- coding: UTF-8 -*-
# editor: JiaYunSong

from PyQt5.QtWidgets import QMainWindow

from DataSource.QueryLog.QueryLogManager import QueryLogManager
from DataSource.Graph.GraphManager import GraphEdges
from DataSource.Sightseeing.SightseeingManager import AttractionSet
from DataSource.FAQsys.FAQRobot import FAQRobot

from MainWindow.Ui import window
from MainWindow.ChildWindows import Set


class Window(QMainWindow):
    def __init__(self, graphPath: str, queryPath: str, sightPath: str, qtxtPath: str, atxtPath: str):
        QMainWindow.__init__(self)

        self.queryLogManager = QueryLogManager(queryPath)
        self.graphManager = GraphEdges(graphPath, self.queryLogManager.addQueryLog)
        self.sightseeingManager = AttractionSet(sightPath, self.graphManager)
        self.FAQRobot = FAQRobot(qtxtPath, atxtPath)

        self.Dialog = window.Ui_Dialog()
        self.Dialog.setupUi(self)

        Set.Running(self)

    def close(self):
        self.queryLogManager.__del__()
        self.sightseeingManager.__del__()
        super().close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    GraphPath = '../DataSource/Graph/Graph.csv'
    QueryPath = '../DataSource/QueryLog/queryLog.history'
    SightPath = '../DataSource/Sightseeing/Sightseeing.csv'
    QtxtPath = '../DataSource/FAQsys/Q.txt'
    AtxtPath = '../DataSource/FAQsys/A.txt'

    app = QApplication(sys.argv)
    mainWindow = Window(GraphPath, QueryPath, SightPath, QtxtPath, AtxtPath)
    mainWindow.show()
    mainWindow.close()
    sys.exit(app.exec_())
