# -*- coding: UTF-8 -*-
# editor: JiaYunSong

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import MainWindow.ChildWindows.ManagerPage.Ui.window


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
        QDialog.__init__(self)
        self.Dialog = MainWindow.ChildWindows.ManagerPage.Ui.window.Ui_Dialog()
        self.Dialog.setupUi(self)

        self.freshAttrTable()
        self.setButtomEvent()
        self.setOthersEvent()

    def Show(self):
        self.show()

    def MesSig(self, s: str) -> None:
        """
        信息栏显示内容更新

        :param s: 信息栏显示的内容
        """
        self.MesBox.setPlainText(f"Message：{s}")

    def freshAttrTable(self, attrList=None):
        """更新景点表格"""
        if attrList is None:
            attrList = list(self.sightseeingManager.attractions.values())

        self.Dialog.Attr_TableWidget.setRowCount(0)
        for attri in attrList:
            row_cnt = self.Dialog.Attr_TableWidget.rowCount()
            self.Dialog.Attr_TableWidget.insertRow(row_cnt)

            self.Dialog.Attr_TableWidget.setItem(row_cnt, 0, QtWidgets.QTableWidgetItem(str(attri.num)))
            self.Dialog.Attr_TableWidget.setItem(row_cnt, 1, QtWidgets.QTableWidgetItem(str(attri.name)))
            self.Dialog.Attr_TableWidget.setItem(row_cnt, 2, QtWidgets.QTableWidgetItem(str(attri.x)))
            self.Dialog.Attr_TableWidget.setItem(row_cnt, 3, QtWidgets.QTableWidgetItem(str(attri.y)))
            self.Dialog.Attr_TableWidget.setItem(row_cnt, 4, QtWidgets.QTableWidgetItem(str(attri.miniIntro)))
            self.Dialog.Attr_TableWidget.setItem(row_cnt, 5, QtWidgets.QTableWidgetItem(str(attri.intro)))
            self.Dialog.Attr_TableWidget.setItem(
                row_cnt, 6,
                QtWidgets.QTableWidgetItem(str(attri.active) if str(attri.active) != "nan" else "无")
            )
        self.freshAttrAllLabel()

    def setButtomEvent(self) -> None:
        """此窗口按钮连接各按钮功能"""
        self.Dialog.AttrSearch_Button.clicked.connect(self.Click_AttrSearch)
        self.Dialog.Add_Button.clicked.connect(self.Click_AttrAdd)
        self.Dialog.AttrUpdate_Button.clicked.connect(self.Click_AttrUpdate)
        self.Dialog.AttrDelete_Button.clicked.connect(self.Click_AttrDelete)

        self.Dialog.PathSearch_Button.clicked.connect(self.Click_PathSearch)
        self.Dialog.PathUpdate_Button.clicked.connect(self.Click_PathUpdate)
        self.Dialog.PathDelete_Button.clicked.connect(self.Click_PathDelete)

        self.Dialog.LogClear_Button.clicked.connect(self.Click_LogClear)

    def setOthersEvent(self) -> None:
        """此窗口其他触发事件实现"""
        self.Dialog.Attr_TableWidget.pressed.connect(self.freshAttrAllLabel)

    def Click_AttrSearch(self):
        InputName = self.Dialog.InputAttrName_TextEdit.toPlainText()
        if InputName == "":
            self.freshAttrTable()
        else:
            attrList = self.sightseeingManager.searchAttractionsInfoByName(InputName)
            self.freshAttrTable(attrList)

    def isNotFillAll(self):
        return self.Dialog.AddName_plainTextEdit.toPlainText() == "" or \
               self.Dialog.AddX_plainTextEdit.toPlainText() == "" or \
               self.Dialog.AddY_plainTextEdit.toPlainText() == "" or \
               self.Dialog.AddMiniIntro_plainTextEdit.toPlainText() == "" or \
               self.Dialog.AddIntro_plainTextEdit.toPlainText() == ""

    def Click_AttrAdd(self):
        if self.isNotFillAll():
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '请填写完整！', QMessageBox.Yes)
            return

        if len(self.sightseeingManager.searchAttractionsInfoByName(
                self.Dialog.AddName_plainTextEdit.toPlainText())) > 0:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '已经存在同名景点！', QMessageBox.Yes)
            return
        Res = self.sightseeingManager.updateAttractionsInfoFromList(
            len(self.sightseeingManager.attractions)+1,
            [
                len(self.sightseeingManager.attractions)+1,
                self.Dialog.AddName_plainTextEdit.toPlainText(),
                int(self.Dialog.AddX_plainTextEdit.toPlainText()),
                int(self.Dialog.AddY_plainTextEdit.toPlainText()),
                self.Dialog.AddMiniIntro_plainTextEdit.toPlainText(),
                self.Dialog.AddIntro_plainTextEdit.toPlainText(),
                self.Dialog.AddActive_plainTextEdit.toPlainText() \
                if self.Dialog.AddActive_plainTextEdit.toPlainText() != "" \
                else "nan"
            ], 1
        )
        self.MesSig(f"添加结果 —— {Res}")
        if Res == "成功！":
            self.freshAttrTable()

    def Click_AttrUpdate(self):
        selectList = self.Dialog.Attr_TableWidget.selectedIndexes()
        if len(selectList) < 1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未选择所需更新项！', QMessageBox.Yes)
            return
        if self.isNotFillAll():
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '请填写完整！', QMessageBox.Yes)
            return
        Res = self.sightseeingManager.updateAttractionsInfoFromList(
            int(selectList[0].data(0)),
            [
                int(selectList[0].data(0)),
                self.Dialog.AddName_plainTextEdit.toPlainText(),
                int(self.Dialog.AddX_plainTextEdit.toPlainText()),
                int(self.Dialog.AddY_plainTextEdit.toPlainText()),
                self.Dialog.AddMiniIntro_plainTextEdit.toPlainText(),
                self.Dialog.AddIntro_plainTextEdit.toPlainText(),
                self.Dialog.AddActive_plainTextEdit.toPlainText() \
                if self.Dialog.AddActive_plainTextEdit.toPlainText() != "" \
                else "nan"
            ], 2)
        self.MesSig(f"更新结果 —— {Res}")
        if Res == "成功！":
            self.freshAttrTable()

    def Click_AttrDelete(self):
        selectList = self.Dialog.Attr_TableWidget.selectedIndexes()
        if len(selectList) < 1:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '未选择所需更新项！', QMessageBox.Yes)
            return
        Res = self.sightseeingManager.updateAttractionsInfoFromList(
            int(selectList[0].data(0)), [25, '白族', 100, 100, 'x', 'x', 'x'], 0)
        self.MesSig(f"删除结果 —— {Res}")
        if Res == "成功！":
            self.freshAttrTable()

    def Click_PathSearch(self):
        st = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.StartingPoint_TextEdit.toPlainText())
        en = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.Destination_TextEdit.toPlainText())
        if len(st) * len(en) == 0:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '起始点或终止点有误！', QMessageBox.Yes)
            return
        length = str(self.graphManager.queryWeightByTwoVertexes(st[0].num-1, en[0].num-1))
        if length == "inf":
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '路径不存在！', QMessageBox.Yes)
            return
        self.Dialog.InputLength_TextEdit.setPlainText(length)

    def Click_PathUpdate(self):
        st = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.StartingPoint_TextEdit.toPlainText())
        en = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.Destination_TextEdit.toPlainText())
        if len(st) * len(en) == 0:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '起始点或终止点有误！', QMessageBox.Yes)
            return
        length = 0
        try:
            length = int(self.Dialog.InputLength_TextEdit.toPlainText())
            Res = self.graphManager.updatePathInfo([st[0].num, en[0].num], length)
            self.MesSig(Res)
        except Exception as e:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', f'路径长度填写有误：{e}！', QMessageBox.Yes)
            return

    def Click_PathDelete(self):
        st = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.StartingPoint_TextEdit.toPlainText())
        en = self.sightseeingManager.searchAttractionsInfoByName(self.Dialog.Destination_TextEdit.toPlainText())
        if len(st) * len(en) == 0:
            QMessageBox.warning(QtWidgets.QDialog(), '提示', '起始点或终止点有误！', QMessageBox.Yes)
        Res = self.graphManager.updatePathInfo((st[0].num, en[0].num))
        self.MesSig(Res)

    def Click_LogClear(self):
        self.queryLogManager.clearAll()
        self.MesSig(f"重置成功！")

    def freshAttrAllLabel(self):
        """通过选取的某行更新Label内容"""
        selectList = self.Dialog.Attr_TableWidget.selectedIndexes()
        if len(selectList) > 0:
            self.Dialog.AddName_plainTextEdit.setPlainText(selectList[1].data(0))
            self.Dialog.AddX_plainTextEdit.setPlainText(selectList[2].data(0))
            self.Dialog.AddY_plainTextEdit.setPlainText(selectList[3].data(0))
            self.Dialog.AddMiniIntro_plainTextEdit.setPlainText(selectList[4].data(0))
            self.Dialog.AddIntro_plainTextEdit.setPlainText(selectList[5].data(0))
            self.Dialog.AddActive_plainTextEdit.setPlainText(
                selectList[6].data(0) if selectList[6].data(0) != "无" else ""
            )
        else:
            self.Dialog.AddName_plainTextEdit.setPlainText("")
            self.Dialog.AddX_plainTextEdit.setPlainText("")
            self.Dialog.AddY_plainTextEdit.setPlainText("")
            self.Dialog.AddMiniIntro_plainTextEdit.setPlainText("")
            self.Dialog.AddIntro_plainTextEdit.setPlainText("")
            self.Dialog.AddActive_plainTextEdit.setPlainText("")
