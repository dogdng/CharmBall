# -*- coding: utf-8 -*-

import os, sys, threading
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QPainter

import utils
from interface import Windows

class FloatBall(QtWidgets.QWidget):
    click_ball = QtCore.Signal(Windows, QPoint) # 信号必须放在方法外面
    ball_radius :int
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowTitle("C&B")
        # 无边框，窗口置顶
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Window)
        # 窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        '''
        悬浮球尺寸和位置
        '''
        screen_size = QtGui.QGuiApplication.primaryScreen().size()
        self.ball_radius = round(min(screen_size.width(), screen_size.height()) * 0.1)
        self.window_size = QSize(self.ball_radius * 2, self.ball_radius * 2)
        self.origin = QPoint(screen_size.width()//2 - self.ball_radius, screen_size.height()//2 - self.ball_radius)
        self.setGeometry(self.origin.x() - self.ball_radius, self.origin.y() - self.ball_radius, self.window_size.width(), self.window_size.height())

        # 设置透明度
        self.setWindowOpacity(0.9)
        # 鼠标手状
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_window_move = True


    def set_origin(self, origin: QPoint):
        '''设置原点：窗口中心坐标'''
        self.origin = origin
        # self.origin = QPoint(960, 540)

    def activate(self) -> None:
        threading.Thread(target=utils.anime_WindowOpacity, args=(self,)).start()
        self.setGeometry(self.origin.x() - self.ball_radius, self.origin.y() - self.ball_radius, self.window_size.width(), self.window_size.height())
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_window_move = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.mouse_pos = event.globalPos()
            self.window_pos = self.pos()
            event.accept() # 将事件标记为已处理

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.is_window_move = False
            diff = event.globalPos() - self.mouse_pos
            new_pos = self.window_pos + diff
            new_pos = utils.limit_window_in_bounds(self.app, new_pos, self.window_size)
            self.move(new_pos)
            self.origin = QPoint(new_pos.x() + self.ball_radius, new_pos.y() + self.ball_radius)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 若菜单已经显示则隐藏
            if self.is_window_move: # 防止move之后还会触发
                # geometry().center()方法获取到的宽度和高度的值每次都会减1，未定位到具体原因
                # self.click_ball.emit(Windows.LEFT, self.geometry().center())
                self.click_ball.emit(Windows.LEFT, self.origin)
            else:
                self.drag_position = None
                event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            event.accept()
            # debug
            sys.exit(0)

    """
    重绘
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Draw rounded rectangle
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect(), self.ball_radius, self.ball_radius)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QtGui.QBrush(QtGui.QColor("#28323B")))

        # 计算三个圆形的圆心坐标
        radius1 = self.ball_radius
        radius2 = round(self.ball_radius * 0.8)
        radius3 = round(self.ball_radius * 0.6)
        x = round(self.width() / 2.0)
        y = round(self.height() / 2.0)
        center = (x, y)

        gradient = QtGui.QRadialGradient(self.rect().center(), self.rect().width() / 2)
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 255))
        gradient.setColorAt(1, QtGui.QColor(200, 200, 200, 255))
        # 绘制三个圆形
        brush1 = QtGui.QBrush(QtGui.QColor("#525F65"))
        brush2 = QtGui.QBrush(QtGui.QColor("#91969C"))
        brush3 = QtGui.QBrush(QtGui.QColor("#FFFFFF"))
        painter.setPen(Qt.PenStyle.NoPen)  # 设置画笔避免边缘黑色

        painter.setBrush(brush1)
        painter.drawEllipse(
            center[0] - radius1, center[1] - radius1, 2 * radius1, 2 * radius1
        )
        painter.setBrush(brush2)
        painter.drawEllipse(
            center[0] - radius2, center[1] - radius2, 2 * radius2, 2 * radius2
        )
        painter.setBrush(brush3)
        painter.drawEllipse(
            center[0] - radius3, center[1] - radius3, 2 * radius3, 2 * radius3
        )
