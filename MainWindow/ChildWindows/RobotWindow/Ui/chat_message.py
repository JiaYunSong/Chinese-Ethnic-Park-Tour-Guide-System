# -*- coding: utf-8 -*-
# editor: Su HanYu,Jia YunSong modified from https://github.com/ShaShiDiZhuanLan/Demo_MessageChat_Qt

import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter as Qpa
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def Get_ImagePath(s: str):
    return os.path.split(os.path.realpath(__file__))[0].replace('\\', '/') + f'/asset/{s}'


class ChatMessage(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        font = self.font()
        font.setPointSize(12)  # 字体大小
        self.setFont(font)
        self.msg = ''
        self.left_avatar_pic = QtGui.QPixmap(Get_ImagePath('left_head.png'))  # 左边头像
        self.right_avatar_pic = QtGui.QPixmap(Get_ImagePath('right_head.png'))  # 右边头像
        self.side = None  # 选择'left' or 'right'

    def rect_cons(self, side):
        minHei = 30
        iconWH = 40
        iconSpaceW = 20
        iconRectW = 5
        iconTMPH = 10
        sanJiaoW = 6
        kuangTMP = 20
        textSpaceRect = 12
        self.side = side
        self.box_w = self.width() - kuangTMP - 2 * (iconWH + iconSpaceW + iconRectW) # 气泡宽度
        self.text_w = self.box_w - 2 * textSpaceRect # 文本宽度
        self.space_w = self.width() - self.text_w

        self.left_avatar = QRect(iconSpaceW, iconTMPH, iconWH, iconWH)
        self.right_avatar = QRect(self.width() - iconSpaceW - iconWH, iconTMPH, iconWH, iconWH)

        size = self.getRealString(self.msg)
        h = minHei if size.height() < minHei else size.height()

        self.left_tri = QRect(
            iconWH + iconSpaceW + iconRectW, int(self.line_h / 2), sanJiaoW,
            int(h - self.line_h))
        # self.right_tri = QRect(
        #     self.width() - iconRectW - iconWH - iconSpaceW - sanJiaoW, int(self.line_h / 2), sanJiaoW,
        #     int(h - self.line_h))

        if size.width() < (self.text_w + self.space_w):
            self.left_box = QRect(self.left_tri.x() + self.left_tri.width(),
                                  int(self.line_h / 4 * 3),
                                  size.width() - self.space_w + 2 * textSpaceRect, int(h - self.line_h))
            self.right_box = QRect(
                self.width() - size.width() + self.space_w - 2 * textSpaceRect - iconWH - iconSpaceW - iconRectW - sanJiaoW,
                int(self.line_h / 4 * 3), size.width() - self.space_w + 2 * textSpaceRect, int(h - self.line_h))
        else:
            self.left_box = QRect(self.left_tri.x() + self.left_tri.width(),
                                  int(self.line_h / 4 * 3),
                                  self.box_w,
                                  int(h - self.line_h))
            self.right_box = QRect(iconWH + kuangTMP + iconSpaceW + iconRectW - sanJiaoW,
                                   int(self.line_h / 4 * 3),
                                   self.box_w,
                                   int(h - self.line_h))

        self.left_text_rect = QRectF(self.left_box.x() + textSpaceRect,
                                     self.left_box.y() + iconTMPH,
                                     self.left_box.width() - 2 * textSpaceRect,
                                     self.left_box.height() - 2 * iconTMPH)
        self.right_text_rect = QRectF(self.right_box.x() + textSpaceRect,
                                      self.right_box.y() + iconTMPH,
                                      self.right_box.width() - 2 * textSpaceRect,
                                      self.right_box.height() - 2 * iconTMPH)

        return QSize(size.width(), h)

    def getRealString(self, src) -> QtCore.QSize:
        fm = QtGui.QFontMetricsF(self.font())
        self.line_h = fm.lineSpacing()
        nCount = src.count("\n")
        nMaxWidth = 0
        if nCount == 0:
            nMaxWidth = fm.width(src)
            value = src
            if nMaxWidth > self.text_w:
                nMaxWidth = self.text_w
                size = int(self.text_w / fm.width(" "))
                num = int(fm.width(value) / self.text_w)
                nCount += num
                temp = ''

                def mid(s, a, n):
                    return s[a:a + n]

                for i in range(num):
                    temp += mid(value, i * size, (i + 1) * size) + '\n'
                src.replace(value, temp)
        else:
            for i in range(nCount + 1):
                value = src.split('\n')[i]
                nMaxWidth = fm.width(value) if fm.width(value) > nMaxWidth else nMaxWidth
                if fm.width(value) > self.text_w:
                    nMaxWidth = self.text_w
                    size = int(self.text_w / fm.width(" "))
                    num = int(fm.width(value) / self.text_w)
                    num = int(((i + num) * fm.width(" ") + fm.width(value)) / self.text_w)
                    nCount += num
                    temp = ""

                    def mid(s, a, n):
                        return s[a:a + n]

                    for j in range(num):
                        temp += mid(value, j * size, (j + 1) * size) + "\n"
                    src.replace(value, temp)
        return QtCore.QSize(nMaxWidth + self.space_w, (nCount + 1) * self.line_h + 2 * self.line_h)

    def _paint(self, text_rect, box_rect, tri_rect, avatar_rect, avatar_pic, color):
        painter = Qpa(self)
        painter.setRenderHint(Qpa.Antialiasing, Qpa.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.gray))
        painter.drawPixmap(avatar_rect, avatar_pic)

        # ----------- box
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(box_rect.x() - 1,
                                box_rect.y() - 1,
                                box_rect.width() + 2,
                                box_rect.height() + 2, 4, 4)
        painter.drawRoundedRect(box_rect, 4, 4)
        # --- triangle
        if tri_rect is not None:
            points = QPolygonF([
                QPointF(tri_rect.x(), 30),
                QPointF(tri_rect.x() + tri_rect.width(), 25),
                QPointF(tri_rect.x() + tri_rect.width(), 35),
            ])
            pen = QPen()
            pen.setColor(color)
            painter.setPen(pen)
            painter.drawPolygon(points, 4)
            painter.drawLine(QPointF(tri_rect.x() - 1, 30),
                             QPointF(tri_rect.x() + tri_rect.width(), 24))
            painter.drawLine(QPointF(tri_rect.x() - 1, 30),
                             QPointF(tri_rect.x() + tri_rect.width(), 36))
            painter.drawLine(
                QPointF(tri_rect.x() + tri_rect.width(), 36),
                QPointF(tri_rect.x() + tri_rect.width(), 24),
            )
        # ----------- kuang finished
        pen = QPen()
        pen.setColor(QColor(51, 51, 51))
        painter.setPen(pen)
        option = QTextOption(Qt.AlignLeft or Qt.AlignVCenter)
        option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        painter.setFont(self.font())
        painter.drawText(text_rect, self.msg, option)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        white = QColor(255, 255, 255)
        blue = QColor(206, 230, 254)
        if self.side == 'left':
            self._paint(
                self.left_text_rect,
                self.left_box,
                self.left_tri,
                self.left_avatar,
                self.left_avatar_pic,
                blue)
        elif self.side == 'right':
            self._paint(
                self.right_text_rect,
                self.right_box,
                None,
                self.right_avatar,
                self.right_avatar_pic,
                white)
