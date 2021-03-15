# -*- coding: UTF-8 -*-
# editor: JiaYunSong

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox

import MainWindow.ChildWindows.PathGuidePage.Ui.window


class Window(QDialog):
    def __init__(self, queryLogManager, graphManager, sightseeingManager, MesBox):
        """
        :param queryLogManager: 主窗口日志管理
        :param graphManager: 主窗口路径管理
        :param sightseeingManager: 主窗口景点管理
        :param MesBox: 主窗口信息栏
        """

        self.MesBox = MesBox
        self.queryLogManager = queryLogManager
        self.graphManager = graphManager
        self.sightseeingManager = sightseeingManager

        # 途经景点的列表
        self.posSelectList = []
        self.disSelectNum = -1

        # 路径列表
        self.pathList = []

        # Map景点距离列表
        self.attrDisList = {}

        QDialog.__init__(self)
        self.Dialog = MainWindow.ChildWindows.PathGuidePage.Ui.window.Ui_Dialog()
        self.Dialog.setupUi(self)

        self.Dialog.DisSelect.setValue(150)
        self.setButtomEvent()
        self.setOthersEvent()
        self.setSightBackground()
        self.freshNowaPosSelectList()
        self.freshHotSight()
        self.freshNearSight()

        self.DotJpg = {'Other': QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlacePointer_Black.png')),
                       'Start': QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlacePointer_Green.png')),
                       'Pos': QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlacePointer_Yellow.png')),
                       'End': QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlacePointer_Red.png'))}
        self.MapSpace = [0, 0, 591, 741]
        self.PlaceNameJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlaceName.png'))
        self.PlaceMapJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('PlaceMap.png'))
        self.NorthPointerJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImgFile('NorthPointer.png'))
        self.freshGraph()
        self.setGraphAction()

        toolStyle = "QToolTip{background-color: white;color: black;border: black solid 1px};"
        self.Dialog.HotSight1.setStyleSheet(toolStyle)
        self.Dialog.HotSight2.setStyleSheet(toolStyle)
        self.Dialog.HotSight3.setStyleSheet(toolStyle)
        self.Dialog.NearSight1.setStyleSheet(toolStyle)
        self.Dialog.NearSight2.setStyleSheet(toolStyle)
        self.Dialog.NearSight3.setStyleSheet(toolStyle)
        self.Dialog.NearSight4.setStyleSheet(toolStyle)
        self.Dialog.Map.setStyleSheet(toolStyle)

    def Show(self):
        # TODO: 不显示地点增删，因为新增的地点无法添加边，算法未考虑，且界面响应略有冲突
        # self.freshNowaPosSelectList()
        self.Dialog.DisSelect.setValue(150)
        self.freshHotSight()
        self.freshNearSight()
        self.freshGraph(True)
        self.setGraphAction()
        self.show()

    def setButtomEvent(self) -> None:
        """此窗口按钮连接各按钮功能"""
        self.Dialog.Search_Button.clicked.connect(self.freshNearSight)

        self.Dialog.HotSight1_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.HotSight1_Name.text()))
        self.Dialog.HotSight2_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.HotSight2_Name.text()))
        self.Dialog.HotSight3_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.HotSight3_Name.text()))
        self.Dialog.NearSight1_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.NearSight1_Name.text()))
        self.Dialog.NearSight2_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.NearSight2_Name.text()))
        self.Dialog.NearSight3_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.NearSight3_Name.text()))
        self.Dialog.NearSight4_Pushbutton.clicked.connect(
            lambda: self.addPosSelectListByName(self.Dialog.NearSight4_Name.text()))

        self.Dialog.CirclePathSelect_Button.clicked.connect(self.SearchCirclePath)
        self.Dialog.ShortestPathSelect_Button.clicked.connect(self.SearchShortestPath)
        self.Dialog.KShortestPathSelect_Button.clicked.connect(self.SearchKShortestPath)
        self.Dialog.DisShortPathSelect_Button.clicked.connect(self.DisShortPath)

    def setOthersEvent(self) -> None:
        """此窗口其他触发事件实现"""
        self.Dialog.PosSelect.currentTextChanged.connect(self.freshNearSight)
        self.Dialog.PosSelect.currentTextChanged.connect(self.freshHotSight)
        self.Dialog.PosSelect.currentTextChanged.connect(lambda: self.freshGraph(True))

    def SearchCirclePath(self):
        """环形路线查询"""
        start = self.getNowaPlaceNum()-1
        if self.disSelectNum != -1 and self.disSelectNum not in self.posSelectList:
            self.posSelectList.append(self.disSelectNum)
            self.disSelectNum = -1
        if len(self.posSelectList) == 0:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未有连接所有节点的直接哈密顿回路！', QMessageBox.Yes)
            return
        cirlist = [i for i in self.posSelectList]
        res = self.graphManager.searchHamilton(start, cirlist)
        if str(res[0]) != 'inf':
            self.pathList = [res[1]]
            self.showPathLength(res[0])
        else:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未有连接各节点的直接哈密顿回路！', QMessageBox.Yes)
        self.freshGraph()

    def SearchShortestPath(self):
        """最短路径查询"""
        start = self.getNowaPlaceNum()-1
        if self.disSelectNum == -1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未选择终点！', QMessageBox.Yes)
            return
        cirlist = [i for i in self.posSelectList]
        res = []
        if len(cirlist) == 0:
            self.pathList = [self.graphManager.searchPathByDijkstra(start, self.disSelectNum)]
            self.showPathLength(self.graphManager.queryDisByTwoVertexes(start, self.disSelectNum))
        else:
            res = self.graphManager.searchHamilton(start, cirlist, self.disSelectNum, False)
            if str(res[0]) != 'inf':
                self.pathList = [res[1]]
                self.showPathLength(res[0])
            else:
                QMessageBox.warning(
                    QtWidgets.QDialog(), '提示',
                    '未有连接各节点的直接哈密顿通路，可多选取经临点以使用优化邻域选择的禁忌搜索求解最优哈密顿回路或通路！',
                    QMessageBox.Yes
                )
        self.freshGraph()

    def SearchKShortestPath(self):
        """k短路径查询"""
        start = self.getNowaPlaceNum()-1
        if self.disSelectNum == -1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未选择终点！', QMessageBox.Yes)
            return
        self.posSelectList = []
        num = self.Dialog.FuncDisSelect.value()
        res = self.graphManager.searchKShortestPath(start, self.disSelectNum, num)
        self.pathList = [i[1] for i in res][::-1]
        self.showPathLength(res[0][0])
        self.freshGraph()

    def DisShortPath(self):
        """适宜距离内路径查询"""
        start = self.getNowaPlaceNum()-1
        if self.disSelectNum == -1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未选择终点！', QMessageBox.Yes)
            return
        self.posSelectList = []
        res = self.graphManager.getAllPaths(start, self.disSelectNum)
        self.pathList = res[::-1]
        self.showPathLength(self.graphManager.queryDisByTwoVertexes(start, self.disSelectNum))
        self.freshGraph()

    def setGraphAction(self):
        """一波之前自研的重载带走图形响应（python就是有这个好处，其他语言做不到）"""

        # 更新Map景点距离列表
        self.attrDisList = {
            (self._fixX(attr.x), self._fixY(attr.y)): attr.num for attr in self.sightseeingManager.attractions.values()
        }

        # TODO: 触发点半径设置
        def mousePressEvent(*args):
            mx = (args[0].x() - self.MapSpace[0])*591/(self.MapSpace[2] - self.MapSpace[0])
            my = (args[0].y() - self.MapSpace[1])*741/(self.MapSpace[3] - self.MapSpace[1])
            if args[0].button() == QtCore.Qt.LeftButton:
                # 左键添加、取消终点
                for x, y in self.attrDisList.keys():
                    if (mx-x)**2 + (my-y)**2 < 36:
                        self.changeDisSelectNum(self.attrDisList[(x, y)]-1)
                        break
            elif args[0].button() == QtCore.Qt.RightButton:
                # 右键添加、取消途经点
                for x, y in self.attrDisList.keys():
                    if (mx-x)**2 + (my-y)**2 < 36:
                        self.addPosSelectList(self.attrDisList[(x, y)]-1)
                        break
            args[0].accept()
        self.Dialog.Map.mousePressEvent = mousePressEvent

        # 设置为移入就实时跟踪鼠标位置
        self.Dialog.Map.setMouseTracking(True)

        def mouseMoveEvent(*args):
            # 判断鼠标位置，给出ToolTip信息
            mx = (args[0].x() - self.MapSpace[0])*591/(self.MapSpace[2] - self.MapSpace[0])
            my = (args[0].y() - self.MapSpace[1])*741/(self.MapSpace[3] - self.MapSpace[1])
            for x, y in self.attrDisList.keys():
                if (mx-x)**2 + (my-y)**2 < 36:
                    self.setSightToolTip(self.Dialog.Map, self.attrDisList[(x, y)])
                    args[0].accept()
                    return
            self.setSightToolTip(self.Dialog.Map)
            args[0].accept()
        self.Dialog.Map.mouseMoveEvent = mouseMoveEvent

        def wheelEvent(*args):
            # TODO: 滚轮放大缩小步长
            step = 20
            # 滚轮缩放
            xk = (args[0].pos().x() - self.MapSpace[0]) / (self.MapSpace[2] - self.MapSpace[0])
            yk = (args[0].pos().y() - self.MapSpace[1]) / (self.MapSpace[3] - self.MapSpace[1])*741/591
            if args[0].angleDelta().y() > 0:
                self.MapSpace = [
                    int(self.MapSpace[0] - step*xk),
                    int(self.MapSpace[1] - step*yk),
                    int(self.MapSpace[2] + step*(1-xk)),
                    int(self.MapSpace[3] + step*(1-yk))
                ]
            else:
                # 缩小
                if self.MapSpace == [0, 0, 591, 741]:
                    return
                self.MapSpace = [
                    int(self.MapSpace[0] + step*xk),
                    int(self.MapSpace[1] + step*yk),
                    int(self.MapSpace[2] - step*(1-xk)),
                    int(self.MapSpace[3] - step*(1-yk))
                ]
                self.MapSpace = [
                    self.MapSpace[0] if self.MapSpace[0] < 0 else 0,
                    self.MapSpace[1] if self.MapSpace[1] < 0 else 0,
                    self.MapSpace[2] if self.MapSpace[2] > 591 else 591,
                    self.MapSpace[3] if self.MapSpace[3] > 741 else 741
                ]
            self.freshGraph()
        self.Dialog.Map.wheelEvent = wheelEvent

    def setSightBackground(self):
        bgJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImage("Hot"))
        self.Dialog.HotSight1_bg.setPixmap(bgJpg)
        self.Dialog.HotSight2_bg.setPixmap(bgJpg)
        self.Dialog.HotSight3_bg.setPixmap(bgJpg)
        bgJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImage("Near"))
        self.Dialog.NearSight1_bg.setPixmap(bgJpg)
        self.Dialog.NearSight2_bg.setPixmap(bgJpg)
        self.Dialog.NearSight3_bg.setPixmap(bgJpg)
        self.Dialog.NearSight4_bg.setPixmap(bgJpg)

    def addPosSelectListByName(self, s: str):
        attrNum = self.sightseeingManager.searchAttractionsInfoByName(s)[0].num
        self.addPosSelectList(attrNum)

    def addPosSelectList(self, num):
        self.pathList = []
        if num in self.posSelectList:
            self.posSelectList.remove(num)
        else:
            if self.disSelectNum != num and self.getNowaPlaceNum()-1 != num:
                self.posSelectList.append(num)
            else:
                QMessageBox.warning(QtWidgets.QDialog(), '提示', '与起点或终点重合，请重新选取！', QMessageBox.Yes)
        self.freshGraph()

    def changeDisSelectNum(self, num):
        self.pathList = []
        if num in self.posSelectList:
            self.posSelectList.remove(num)
        if num == self.getNowaPlaceNum()-1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '与起点重合，请重新选取！', QMessageBox.Yes)
        else:
            self.disSelectNum = num
        self.freshGraph()

    def freshNowaPosSelectList(self):
        self.Dialog.PosSelect.clear()

        attrList = list(self.sightseeingManager.attractions.values())
        for attri in attrList:
            self.Dialog.PosSelect.addItem(attri.name)

    def getNowaPlaceNum(self):
        attrName = self.Dialog.PosSelect.currentText()
        attr = None
        for ai in list(self.sightseeingManager.attractions.values()):
            if ai.name == attrName:
                attr = ai
                break
        return attr.num

    def freshGraph(self, clear=False):
        """显示地图"""
        if clear:
            self.posSelectList = []
            self.disSelectNum = -1
            self.pathList = []

        # 强行重载
        def paintEvent(*args):
            painter = QtGui.QPainter(self.Dialog.Map)
            painter.begin(self.Dialog.Map)

            painter.drawPixmap(
                self.MapSpace[0], self.MapSpace[1],
                self.MapSpace[2]-self.MapSpace[0], self.MapSpace[3]-self.MapSpace[1],
                self.PlaceMapJpg)
            self.drawGraphAllEdge(painter)
            self.drawGraphAllDot(painter)
            painter.drawPixmap(
                self.MapSpace[0], self.MapSpace[1],
                self.MapSpace[2]-self.MapSpace[0], self.MapSpace[3]-self.MapSpace[1],
                self.PlaceNameJpg)
            painter.drawPixmap(510, 20, 60, 400, self.NorthPointerJpg)

            painter.end()
        self.Dialog.Map.paintEvent = paintEvent
        self.Dialog.Map.repaint()

    def _fixX(self, x):
        return (int(x * 1.2)+100)*(self.MapSpace[2] - self.MapSpace[0])/591 + self.MapSpace[0]

    def _fixY(self, y):
        return (741-int(y * 1.2)-20)*(self.MapSpace[3] - self.MapSpace[1])/741 + self.MapSpace[1]

    def drawGraphAllDot(self, painter: QtGui.QPainter):
        attrList = list(self.sightseeingManager.attractions.values())
        for attri in attrList:
            self.drawGraphDot(attri.name, attri.x, attri.y, 'Other', painter)

        start = self.sightseeingManager.searchAttractionsInfo(self.getNowaPlaceNum())
        self.drawGraphDot(start.name, start.x, start.y, 'Start', painter)

        pos = [self.sightseeingManager.searchAttractionsInfo(i+1) for i in self.posSelectList]
        for attri in pos:
            self.drawGraphDot(attri.name, attri.x, attri.y, 'Pos', painter)

        if self.disSelectNum != -1:
            end = self.sightseeingManager.searchAttractionsInfo(self.disSelectNum+1)
            self.drawGraphDot(end.name, end.x, end.y, 'End', painter)

    def drawGraphDot(self, name: str, x: int, y: int, Type: str, painter: QtGui.QPainter):
        # TODO: 地点文字贴背景上

        x = self._fixX(x)
        y = self._fixY(y)

        painter.drawPixmap(x-12, y-23, 25, 25, self.DotJpg[Type])
        painter.setPen(QtCore.Qt.red)

    def drawGraphAllEdge(self, painter: QtGui.QPainter):
        # 绘制所有边
        for x, y, length, _ in self.graphManager.edges[1:]:
            if str(length) == 'inf':
                continue
            startAttr = self.sightseeingManager.searchAttractionsInfo(x+1)
            endAttr = self.sightseeingManager.searchAttractionsInfo(y+1)
            self.drawGraphEdge(startAttr.x, startAttr.y, endAttr.x, endAttr.y,
                               QtGui.QColor(200, 200, 200, 255), painter)

        num = len(self.pathList)
        if num == 0:
            self.showPathLength(0)
            return

        # 绘制路径
        for path, hue in zip(self.pathList, range(0, 359, 359//num)[:num]):
            color = QtGui.QColor.fromHsv(hue, 255, 255)
            for x, y in zip(path[1:], path[:-1]):
                startAttr = self.sightseeingManager.searchAttractionsInfo(x + 1)
                endAttr = self.sightseeingManager.searchAttractionsInfo(y + 1)
                self.drawGraphEdge(startAttr.x, startAttr.y, endAttr.x, endAttr.y, color, painter)

    def drawGraphEdge(self, xx: int, xy: int, yx: int, yy: int, Color: QtGui.QColor, painter: QtGui.QPainter):
        pen = painter.pen()
        pen.setColor(Color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(self._fixX(xx), self._fixY(xy), self._fixX(yx), self._fixY(yy))

    def showPathLength(self, length: int):
        self.Dialog.pathLength_Text.setText(str(length))
        self.Dialog.pathClock_Text.setText(str(int(length / 0.6)/100))

    def freshNearSight(self):
        start = self.getNowaPlaceNum()
        distance = self.Dialog.DisSelect.value()
        placeList = [i[0] for i in self.graphManager.SearchWithinDistance(start-1, distance)]
        num = len(placeList)
        if num > 4:
            placeList = placeList[:4]
            for pi, num in zip(placeList, range(4)):
                self.fillSightToWidget(False, num + 1, pi + 1)
        else:
            for pi, ni in zip(placeList, range(num)):
                self.fillSightToWidget(False, ni+1, pi + 1)
            for ni in range(num, 4):
                self.fillSightToWidget(False, ni+1)

    def freshHotSight(self):
        hotList = self.queryLogManager.SearchRecommendAttraction(self.getNowaPlaceNum()-1)
        for hot, num in zip(hotList, range(3)):
            self.fillSightToWidget(True, num+1, hot[0]+1)

    def fillSightToWidget(self, isHot: bool, fillNum, Sightnum=None):
        sType = "Hot" if isHot else "Near"
        if Sightnum is None:
            exec(f"""
self.setSightToolTip(self.Dialog.{sType}Sight{fillNum}_Pushbutton)
self.Dialog.{sType}Sight{fillNum}.setVisible(False)""")
            return

        SightJpg = QtGui.QPixmap(self.sightseeingManager.SearchAttractionsImage(Sightnum-1))
        attr = self.sightseeingManager.searchAttractionsInfo(Sightnum)
        exec(f"""
self.Dialog.{sType}Sight{fillNum}.setVisible(True)
self.Dialog.{sType}Sight{fillNum}_Name.setText(attr.name)
self.Dialog.{sType}Sight{fillNum}_Text.setText(attr.miniIntro)
self.setSightToolTip(self.Dialog.{sType}Sight{fillNum}_Pushbutton, Sightnum)
self.Dialog.{sType}Sight{fillNum}_JPG.setPixmap(SightJpg)""")

    def setSightToolTip(self, Pushbutton, num=None):
        if num is None:
            Pushbutton.setToolTip('')
            return
        attr = self.sightseeingManager.searchAttractionsInfo(num)
        Pushbutton.setToolTip(
            self.getToolTipMes(
                attr.name,
                attr.intro,
                str(attr.active),
                self.sightseeingManager.SearchAttractionsImage(num-1)
            )
        )

    @staticmethod
    def getToolTipMes(Name, Intro, Active, JPGSource):
        ad = ""
        if Active != "nan":
            ac = Active.split('*')
            for av in ac:
                av = av.split('/')
                ad = f"{ad}<tr><td>{av[1]}</td><td>{av[0]}</td></tr>"

        return f"""<html><head/>
        <body>
            <span style=\" font-size:x-large; font-weight:600;\">{Name}</span>
            <p>景点介绍：{Intro}</p>
            <p>
                <img src=\"{JPGSource}\" width=\"300\" height=\"300\"/>
            </p>
""" + (r"""
        <style type="text/css">
        table.gridtable {
            font-family: verdana,arial,sans-serif;
            font-size:15px;
            color:#333333;
            border-width: 1px;
            border-color: #666666;
            border-collapse: collapse;
        }
        table.gridtable th {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #dedede;
        }
        table.gridtable td {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #ffffff;
        }
""" + f"""
        </style>
        <!-- Table goes in the document BODY -->
        <table class="gridtable">
        <tr>
            <th>活动名称</th><th>举行的时间</th>
        </tr>
        {ad}
        </table>
""" if Active != "nan" else "") + """
        </body></html>"""
