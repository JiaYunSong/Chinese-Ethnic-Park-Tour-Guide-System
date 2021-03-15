# -*- coding: UTF-8 -*-
# editor: JiaYunSong

import MainWindow.ChildWindows.PathGuidePage.Class
import MainWindow.ChildWindows.ManagerPage.Class
import MainWindow.ChildWindows.RobotWindow.Class
import MainWindow.ChildWindows.SchedulingPage.Class


def Running(parentWindow):
    """
    建立父窗口与子窗口的连接
    :param parentWindow: 父窗口对象
    """

    def pageSetting(pWindow, cWindow, num):
        pWindow.Dialog.Module_stackedWidget.setCurrentIndex(num)
        cWindow.Show()

    # “景点导览”按钮窗口导入
    parentWindow.Dialog.page01 = MainWindow.ChildWindows.PathGuidePage.Class.Window(
        parentWindow.queryLogManager,
        parentWindow.graphManager,
        parentWindow.sightseeingManager,
        parentWindow.Dialog.Mes_plainTextEdit
    )
    parentWindow.Dialog.Module_stackedWidget.addWidget(parentWindow.Dialog.page01)
    parentWindow.Dialog.PathGuide_Button.clicked.connect(
        lambda: pageSetting(parentWindow, parentWindow.Dialog.page01, 0))

    # “信息管理”按钮窗口导入
    parentWindow.Dialog.page02 = MainWindow.ChildWindows.ManagerPage.Class.Window(
        parentWindow.queryLogManager,
        parentWindow.graphManager,
        parentWindow.sightseeingManager,
        parentWindow.Dialog.Mes_plainTextEdit
    )
    parentWindow.Dialog.Module_stackedWidget.addWidget(parentWindow.Dialog.page02)
    parentWindow.Dialog.Mange_Button.clicked.connect(
        lambda: pageSetting(parentWindow, parentWindow.Dialog.page02, 1))

    # “智慧问答”按钮窗口导入
    parentWindow.Dialog.page03 = MainWindow.ChildWindows.RobotWindow.Class.Window(
        parentWindow.FAQRobot, parentWindow.Dialog.Mes_plainTextEdit)
    parentWindow.Dialog.Module_stackedWidget.addWidget(parentWindow.Dialog.page03)
    parentWindow.Dialog.QA_Button.clicked.connect(
        lambda: pageSetting(parentWindow, parentWindow.Dialog.page03, 2))

    # “精准调度”按钮窗口导入
    parentWindow.Dialog.page04 = MainWindow.ChildWindows.SchedulingPage.Class.Window(
        parentWindow.Dialog.Mes_plainTextEdit)
    parentWindow.Dialog.Module_stackedWidget.addWidget(parentWindow.Dialog.page04)
    parentWindow.Dialog.Optimize_Button.clicked.connect(
        lambda: pageSetting(parentWindow, parentWindow.Dialog.page04, 3))
