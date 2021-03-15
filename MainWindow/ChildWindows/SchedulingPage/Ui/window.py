# -*- coding: utf-8 -*-
# editor: JiaYunSong
# Created by: PyQt5 UI code generator 5.15.0


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1301, 781)
        self.Scheduling_groupBox = QtWidgets.QGroupBox(Dialog)
        self.Scheduling_groupBox.setGeometry(QtCore.QRect(50, 40, 1201, 691))
        self.Scheduling_groupBox.setStyleSheet("border:1px solid black")
        self.Scheduling_groupBox.setObjectName("Scheduling_groupBox")
        self.Input01_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input01_TextEdit.setGeometry(QtCore.QRect(330, 100, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input01_TextEdit.setFont(font)
        self.Input01_TextEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Input01_TextEdit.setAcceptRichText(False)
        self.Input01_TextEdit.setObjectName("Input01_TextEdit")
        self.Search_Button = QtWidgets.QPushButton(self.Scheduling_groupBox)
        self.Search_Button.setGeometry(QtCore.QRect(720, 550, 101, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Search_Button.setFont(font)
        self.Search_Button.setStyleSheet("QPushButton {background-color : #FFF;} \n"
"QPushButton:hover{background-color: #DDD;}\n"
"QPushButton:pressed {background-color: #00000000;}")
        self.Search_Button.setObjectName("Search_Button")
        self.Describe01_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe01_Label.setGeometry(QtCore.QRect(70, 100, 131, 31))
        self.Describe01_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt ;")
        self.Describe01_Label.setObjectName("Describe01_Label")
        self.Describe02_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe02_Label.setGeometry(QtCore.QRect(70, 190, 211, 31))
        self.Describe02_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe02_Label.setObjectName("Describe02_Label")
        self.Describe03_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe03_Label.setGeometry(QtCore.QRect(70, 280, 221, 31))
        self.Describe03_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);font: 12pt;")
        self.Describe03_Label.setObjectName("Describe03_Label")
        self.Describe04_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe04_Label.setGeometry(QtCore.QRect(70, 370, 211, 31))
        self.Describe04_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe04_Label.setObjectName("Describe04_Label")
        self.Describe05_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe05_Label.setGeometry(QtCore.QRect(70, 460, 221, 31))
        self.Describe05_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe05_Label.setObjectName("Describe05_Label")
        self.Describe06_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe06_Label.setGeometry(QtCore.QRect(70, 550, 281, 31))
        self.Describe06_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe06_Label.setObjectName("Describe06_Label")
        self.Input02_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input02_TextEdit.setGeometry(QtCore.QRect(330, 190, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input02_TextEdit.setFont(font)
        self.Input02_TextEdit.setAcceptRichText(False)
        self.Input02_TextEdit.setObjectName("Input02_TextEdit")
        self.Unit01_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit01_Label.setGeometry(QtCore.QRect(540, 100, 71, 31))
        self.Unit01_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit01_Label.setObjectName("Unit01_Label")
        self.Input03_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input03_TextEdit.setGeometry(QtCore.QRect(330, 280, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input03_TextEdit.setFont(font)
        self.Input03_TextEdit.setAcceptRichText(False)
        self.Input03_TextEdit.setObjectName("Input03_TextEdit")
        self.Input04_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input04_TextEdit.setGeometry(QtCore.QRect(330, 370, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input04_TextEdit.setFont(font)
        self.Input04_TextEdit.setAcceptRichText(False)
        self.Input04_TextEdit.setObjectName("Input04_TextEdit")
        self.Input05_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input05_TextEdit.setGeometry(QtCore.QRect(330, 460, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input05_TextEdit.setFont(font)
        self.Input05_TextEdit.setAcceptRichText(False)
        self.Input05_TextEdit.setObjectName("Input05_TextEdit")
        self.Input06_TextEdit = QtWidgets.QTextEdit(self.Scheduling_groupBox)
        self.Input06_TextEdit.setGeometry(QtCore.QRect(380, 550, 161, 31))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.Input06_TextEdit.setFont(font)
        self.Input06_TextEdit.setStyleSheet("")
        self.Input06_TextEdit.setAcceptRichText(False)
        self.Input06_TextEdit.setObjectName("Input06_TextEdit")
        self.Unit02_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit02_Label.setGeometry(QtCore.QRect(540, 190, 91, 31))
        self.Unit02_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit02_Label.setObjectName("Unit02_Label")
        self.Unit04_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit04_Label.setGeometry(QtCore.QRect(540, 280, 71, 31))
        self.Unit04_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit04_Label.setObjectName("Unit04_Label")
        self.Unit03_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit03_Label.setGeometry(QtCore.QRect(540, 370, 71, 31))
        self.Unit03_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit03_Label.setObjectName("Unit03_Label")
        self.Unit05_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit05_Label.setGeometry(QtCore.QRect(540, 460, 91, 31))
        self.Unit05_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit05_Label.setObjectName("Unit05_Label")
        self.Unit06_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit06_Label.setGeometry(QtCore.QRect(580, 550, 71, 31))
        self.Unit06_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt \"Adilla and Rita\";")
        self.Unit06_Label.setObjectName("Unit06_Label")
        self.Describe08_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe08_Label.setGeometry(QtCore.QRect(720, 480, 121, 31))
        self.Describe08_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe08_Label.setObjectName("Describe08_Label")
        self.Describe07_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Describe07_Label.setGeometry(QtCore.QRect(720, 420, 51, 31))
        self.Describe07_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Describe07_Label.setObjectName("Describe07_Label")
        self.Unit08_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit08_Label.setGeometry(QtCore.QRect(940, 480, 51, 31))
        self.Unit08_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Unit08_Label.setObjectName("Unit08_Label")
        self.Unit07_Label = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Unit07_Label.setGeometry(QtCore.QRect(880, 420, 271, 31))
        self.Unit07_Label.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"font: 12pt;")
        self.Unit07_Label.setObjectName("Unit07_Label")
        self.Output_Label_2 = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Output_Label_2.setGeometry(QtCore.QRect(830, 470, 111, 51))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.Output_Label_2.setFont(font)
        self.Output_Label_2.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 0, 0);")
        self.Output_Label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Output_Label_2.setObjectName("Output_Label_2")
        self.Output_Label_1 = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.Output_Label_1.setGeometry(QtCore.QRect(770, 410, 121, 51))
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")  # 原来是 Adilla and Rita 字体
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.Output_Label_1.setFont(font)
        self.Output_Label_1.setStyleSheet("border-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 0, 0);")
        self.Output_Label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.Output_Label_1.setObjectName("Output_Label_1")
        self.widget = QtWidgets.QLabel(self.Scheduling_groupBox)
        self.widget.setGeometry(QtCore.QRect(720, 10, 400, 400))
        self.widget.setStyleSheet("border-color: rgba(255, 255, 255, 0);")
        self.widget.setObjectName("widget")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Scheduling_groupBox.setTitle(_translate("Dialog", "调度信息"))
        self.Search_Button.setText(_translate("Dialog", "查询"))
        self.Describe01_Label.setText(_translate("Dialog", "当前景点票价"))
        self.Describe02_Label.setText(_translate("Dialog", "当前景点一小时客流量"))
        self.Describe03_Label.setText(_translate("Dialog", "当前景点排队容量上限"))
        self.Describe04_Label.setText(_translate("Dialog", "预计单次游览完成时间"))
        self.Describe05_Label.setText(_translate("Dialog", "雇佣一名导游所需费用"))
        self.Describe06_Label.setText(_translate("Dialog", "当前景点可雇佣最大导游数目"))
        self.Unit01_Label.setText(_translate("Dialog", "元/人"))
        self.Unit02_Label.setText(_translate("Dialog", "人/小时"))
        self.Unit04_Label.setText(_translate("Dialog", "人"))
        self.Unit03_Label.setText(_translate("Dialog", "分钟"))
        self.Unit05_Label.setText(_translate("Dialog", "元/小时"))
        self.Unit06_Label.setText(_translate("Dialog", "人"))
        self.Describe08_Label.setText(_translate("Dialog", "最大收益为"))
        self.Describe07_Label.setText(_translate("Dialog", "雇佣"))
        self.Unit08_Label.setText(_translate("Dialog", "元"))
        self.Unit07_Label.setText(_translate("Dialog", "名导游可使当前景点收益最大"))
        self.Output_Label_2.setText(_translate("Dialog", "0"))
        self.Output_Label_1.setText(_translate("Dialog", "0"))