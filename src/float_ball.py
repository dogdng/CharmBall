# -*- coding: utf-8 -*-

import os, PySide6
import sys, threading
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from left_click_window import LeftClickWindow
from utils import *

class FloatBall(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.tray_icon = QSystemTrayIcon(self)
        self.left_click_window = LeftClickWindow()

        self.setWindowTitle("C&B")
        # 无边框，窗口置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
        # 窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        '''
        悬浮球尺寸和位置
        '''
        screen_size = QGuiApplication.primaryScreen().size()
        button_width = screen_size.width()/20
        button_height = screen_size.height()/20
        button_x = (screen_size.width() - button_width)/2
        button_y = (screen_size.height() - button_height)/2
        self.setGeometry(button_x, button_y, button_width, button_height)

        # 设置透明度
        self.setWindowOpacity(0.9)
        # 鼠标手状
        self.setCursor(Qt.PointingHandCursor)

        # 系统托盘
        self.config_tray()

        # 真则表示鼠标在本次点击后为发生拖动
        self.mouse_flag = True

    def config_tray(self):
        self.tray_icon.setIcon(QIcon("./resources/EasingFunctionsIcon.png"))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        # self.tray_icon.show()

        # 创建右键菜单
        self.tray_menu = QMenu(self)
        self.close_action = QAction("退出", self)
        self.close_action.triggered.connect(QCoreApplication.quit)
        self.tray_menu.addAction(self.close_action)

        # 将右键菜单添加到系统托盘图标
        self.tray_icon.setContextMenu(self.tray_menu)

        # 显示系统托盘图标
        self.tray_icon.show()
        # 指示窗口状态，True表示仅显示A窗口，False表示仅显示B窗口
        self.tray_flag = True

    """
    系统托盘
    """

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                if self.tray_flag:
                    self.show()
                else:
                    if self.left_click_window.isVisible():
                        self.left_click_window.hide()
                    else:
                        self.left_click_window.show()

    """
    鼠标事件
    """

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_flag = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            # 范围判定用
            self.mouse_pos = event.globalPos()
            self.window_pos = self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.mouse_flag = False

            focus_screen = get_focus_screen(self.app)
            # 获取焦点屏幕的参数
            f_screen_geometry = focus_screen.geometry()
            f_x, f_y, f_width, f_height = (
                f_screen_geometry.x(),
                f_screen_geometry.y(),
                f_screen_geometry.width(),
                f_screen_geometry.height(),
            )
            f_scale_factor = get_devicePixelRatio(focus_screen)
            # f_scale_factor = focus_screen.devicePixelRatio()
            # 考虑缩放后要四舍五入，系统问题，不一定是整数
            f_xrb = round(f_x + f_width * f_scale_factor)
            f_yrb = round(f_y + f_height * f_scale_factor)

            # 对新位置进行范围限制,如果拖动到另一块屏幕，则会改变焦点屏幕从而直接跳到另一屏幕，所以不需要进行上下左右有无屏幕的判断了
            max_x = focus_screen.geometry().right() - self.width()
            max_y = focus_screen.geometry().bottom() - self.height()

            diff = event.globalPos() - self.mouse_pos
            new_pos = self.window_pos + diff

            if new_pos.x() < focus_screen.geometry().left():
                new_pos.setX(focus_screen.geometry().left())
            elif new_pos.x() > max_x:
                new_pos.setX(max_x)

            if new_pos.y() < focus_screen.geometry().top():
                new_pos.setY(focus_screen.geometry().top())
            elif new_pos.y() > max_y:
                new_pos.setY(max_y)

            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        window_b_width = 202
        window_b_height = 498
        if event.button() == Qt.LeftButton:
            # 若菜单已经显示则隐藏
            if self.mouse_flag:
                self.tray_flag = False
                self.hide()

                focus_screen = get_focus_screen(self.app)
                f_screen_geometry = focus_screen.geometry()

                # 获取焦点屏幕的参数
                f_screen_geometry = focus_screen.geometry()
                f_x, f_y, f_width, f_height = (
                    f_screen_geometry.x(),
                    f_screen_geometry.y(),
                    f_screen_geometry.width(),
                    f_screen_geometry.height(),
                )
                f_scale_factor = get_devicePixelRatio(focus_screen)
                # f_scale_factor = focus_screen.devicePixelRatio()
                # 考虑缩放后要四舍五入，系统问题，不一定是整数
                f_xrb = round(f_x + f_width * f_scale_factor)
                f_yrb = round(f_y + f_height * f_scale_factor)

                # 约束新生成的windwosB的位置，防止windowB部分直接生成在不可见区域
                max_x = focus_screen.geometry().right() - self.width()
                max_y = focus_screen.geometry().bottom() - self.height()

                n_pos = [
                    self.geometry().center().x() - self.left_click_window.width() / 2,
                    self.geometry().center().y() - self.left_click_window.height() / 2,
                ]

                if n_pos[0] < focus_screen.geometry().left():
                    n_pos[0] = focus_screen.geometry().left()
                elif n_pos[0] + window_b_width > max_x:
                    n_pos[0] = max_x - window_b_width

                if n_pos[1] < focus_screen.geometry().top():
                    n_pos[1] = focus_screen.geometry().top()
                elif n_pos[1] + window_b_height > max_y:
                    n_pos[1] = max_y + self.height() - window_b_height

                self.left_click_window.setGeometry(
                    QRect(n_pos[0], n_pos[1], window_b_width, window_b_height)
                )

                threading.Thread(
                    target=anime_WindowOpacity, args=(self.left_click_window,)
                ).start()

                self.left_click_window.show()
            else:
                self.drag_position = None
                event.accept()

    """
    重绘
    """

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw rounded rectangle
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 25, 25)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QBrush(QColor("#28323B")))

        # 计算三个圆形的圆心坐标
        radius1 = 52
        radius2 = 44
        radius3 = 36
        x = self.width() // 2
        y = self.height() // 2
        center1 = (x, y)

        gradient = QRadialGradient(self.rect().center(), self.rect().width() / 2)
        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(1, QColor(200, 200, 200, 255))
        # 绘制三个圆形
        brush1 = QBrush(QColor("#525F65"))
        brush2 = QBrush(QColor("#91969C"))
        brush3 = QBrush(QColor("#FFFFFF"))
        painter.setPen(Qt.NoPen)  # 设置画笔避免边缘黑色

        painter.setBrush(brush1)
        painter.drawEllipse(
            center1[0] - radius1, center1[1] - radius1, 2 * radius1, 2 * radius1
        )
        painter.setBrush(brush2)
        painter.drawEllipse(
            center1[0] - radius2, center1[1] - radius2, 2 * radius2, 2 * radius2
        )
        painter.setBrush(brush3)
        painter.drawEllipse(
            center1[0] - radius3, center1[1] - radius3, 2 * radius3, 2 * radius3
        )
