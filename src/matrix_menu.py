# -*- coding: utf-8 -*-

import os, sys, threading
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QIcon, QPainter, QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout

import utils, interface

from images.closemenu_png import img as closemenu_png
from images.mission_png import img as mission_png
from images.screen_png import img as screen_png
from images.desktop_png import img as desktop_png



class MatrixMenu(QWidget):
    '单击功能窗口'
    switch_default = QtCore.Signal(interface.Windows, QPoint) # 信号必须放在方法外面
    origin = QPoint()
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Matrix Menu")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                            | Qt.WindowType.WindowStaysOnTopHint
                            # | Qt.WindowType.Popup
                            | Qt.WindowType.Window
                            | Qt.WindowType.Tool)

        # self.origin
        self.window_size = QSize(202, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setGeometry(self.origin.x() - round(self.window_size.width()/2), self.origin.y() - round(self.window_size.height()/2), self.window_size.width(), self.window_size.height())
        self.setWindowOpacity(0.9)

        self.add_buttons()

    def set_origin(self, origin: QPoint):
        '''设置原点：窗口中心坐标'''
        self.origin = origin

    def get_icon(self, img_data):
        '''通过base64编码的图片字符串获取QIcon对象'''
        data = QtCore.QByteArray().fromBase64(img_data)
        image = QtGui.QImage()
        image.loadFromData(data)
        pix = QtGui.QPixmap.fromImage(image)
        return QIcon(pix)


    def add_buttons(self):
        # 设置布局
        # 一个垂直布局，第一层、第三层套两个网格布局，第二层放Slider
        # 设置布局为垂直居中对齐
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignJustify) #AlignCenter)


        # 按钮样式
        button_style = """
        QPushButton {
            background-color: #FFFFFF;
            border: 2px;
            border-radius: 10px;
            color: #FFFFFF;
            font-size: 16px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #91969C;
        }
        QPushButton:pressed {
            background-color: #525F65;
        }
        """

        self.button1 = MyQPushButton(self)
        self.button1.setIcon(self.get_icon(mission_png))
        self.button1.setIconSize(QSize(50, 50))
        self.button1.setFixedSize(50, 50)
        self.button1.clicked.connect(self.mission_view)
        layout.addWidget(self.button1, 0, 0)
        self.button1.setStyleSheet(button_style)

        self.close_button = MyQPushButton(self)
        self.close_button.setIcon(self.get_icon(closemenu_png))
        self.close_button.setIconSize(QSize(50, 50))
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.switch_to_default_window)
        layout.addWidget(self.close_button, 0, 1)
        self.close_button.setStyleSheet(button_style)

        self.button3 = MyQPushButton(self)

        self.button3.setIcon(self.get_icon(screen_png))
        self.button3.setIconSize(QSize(50, 50))
        self.button3.setFixedSize(50, 50)
        self.button3.clicked.connect(self.change_screen)
        layout.addWidget(self.button3, 0, 2)
        self.button3.setStyleSheet(button_style)


        self.button6 = MyQPushButton(self)
        self.button6.setIcon(self.get_icon(desktop_png))
        self.button6.setIconSize(QSize(50, 50))
        self.button6.setFixedSize(50, 50)
        self.button6.clicked.connect(self.back_desktop)
        layout.addWidget(self.button6, 1, 0)
        self.button6.setStyleSheet(button_style)

        self.button7 = MyQPushButton(self)
        self.button7.setIcon(QIcon("./resources/taskmgr.png"))
        self.button7.setIconSize(QSize(50, 50))
        self.button7.setFixedSize(50, 50)
        self.button7.clicked.connect(self.open_taskmgr)
        layout.addWidget(self.button7, 1, 1)
        self.button7.setStyleSheet(button_style)

        self.button8 = MyQPushButton(self)
        self.button8.setIcon(QIcon("./resources/utools.png"))
        self.button8.setIconSize(QSize(45, 45))
        self.button8.setFixedSize(50, 50)
        self.button8.clicked.connect(self.open_utools)
        layout.addWidget(self.button8, 1, 2)
        self.button8.setStyleSheet(button_style)

        self.button9 = MyQPushButton(self)
        self.button9.setIcon(QIcon("./resources/screenshot.png"))
        self.button9.setIconSize(QSize(50, 50))
        self.button9.setFixedSize(50, 50)
        self.button9.clicked.connect(self.take_screenshot)
        layout.addWidget(self.button9, 2, 1)
        self.button9.setStyleSheet(button_style)

        self.button91 = MyQPushButton(self)
        self.button91.setIcon(QIcon("./resources/screenshot.png"))
        self.button91.setIconSize(QSize(50, 50))
        self.button91.setFixedSize(50, 50)
        self.button91.clicked.connect(self.take_screenshot)
        layout.addWidget(self.button91, 3, 2)
        self.button91.setStyleSheet(button_style)

        self.setLayout(layout)

    """
    鼠标事件
    """
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_flag = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            # 范围判定用
            self.mouse_pos = event.globalPos()
            self.window_pos = self.pos()
            self.switch_to_default_window()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print(self.width(),self.height())
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.mouse_flag = False
            diff = event.globalPos() - self.mouse_pos
            new_pos = self.window_pos + diff
            new_pos = utils.limit_window_in_bounds(self.app, new_pos, QSize(self.width(), self.height()))
            self.move(new_pos)
            self.origin = QPoint(new_pos.x() + round(self.width()/2), new_pos.y() + round(self.height()/2))
            event.accept()

    def wheelEvent(self, event):
        print(f"滚轮:{event.angleDelta()}")

    def activate(self) -> None:
        n_pos = QPoint(self.origin.x() - round(self.width() / 2), self.origin.y() - round(self.height() / 2))
        n_pos = utils.limit_window_in_bounds(self.app, n_pos, QSize(self.width(), self.height()))
        self.setGeometry(n_pos.x(), n_pos.y(), self.window_size.width(), self.window_size.height())
        threading.Thread(
            target=utils.anime_WindowOpacity, args=(self,)
        ).start()
        self.show()

    """
    重绘
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        # 设置画笔避免边缘黑色
        painter.setPen(Qt.PenStyle.NoPen)
        # Draw rounded rectangle
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect(), 25, 25)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QtGui.QBrush(QtGui.QColor("#28323B")))

    """
    按钮槽函数
    """
    def switch_to_default_window(self):
        self.switch_default.emit(interface.Windows.DEFAULT, self.origin)

    def mission_view(self):
        pass

    def open_taskmgr(self):
        pass


    def change_screen(self):
        pass

    def back_desktop(self):
        pass

    def open_utools(self):
        pass

    def take_screenshot(self):
        pass



# 滚动区域控件
class ScrollableButtonGrid(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # 创建一个网格布局，用于添加按钮
        self.g_layout = QGridLayout()
        self.g_layout.setSpacing(20)

        # 创建一个滚动区域，将水平布局添加到其中
        self.scroll_area = MyScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.g_layout)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        # 设定初始位置
        self.scroll_area.horizontalScrollBar().setValue(0)

        # 创建一个垂直布局，将滚动区域添加到其中
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.scroll_area)

        # 将垂直布局设置为主窗口的布局
        self.setLayout(self.v_layout)

        self.mouse_pos = None

    def wheelEvent(self, event):
        # 忽略滚轮事件
        event.accept()

    def mousePressEvent(self, event):
        # 记录鼠标按下时的位置
        self.mouse_pos = QCursor.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            # 计算鼠标拖动的距离
            delta = QCursor.pos() - self.mouse_pos

            # 计算滚动条应该滚动到的位置
            scrollbar = self.scroll_area.horizontalScrollBar()
            value = scrollbar.value() - delta.x()

            # 设置滚动条的位置
            scrollbar.setValue(value)

            # 更新鼠标位置
            self.mouse_pos = QCursor.pos()

    def mouseReleaseEvent(self, event):
        # 清除已经记录的鼠标位置
        self.mouse_pos = None

        # 保证位置是60的整数倍
        scrollbar = self.scroll_area.horizontalScrollBar()
        value = scrollbar.value()
        scrollbar.setValue(value)
        scrollbar.setValue(round(value / 70) * 70)

    def __init__(self):
        super().__init__()

        # self.setStyleSheet('''QScrollArea {border: none;}''')
        # self.setStyleSheet("background-color: transparent;")

        # 创建一个网格布局，用于添加按钮
        self.g_layout = QtWidgets.QGridLayout()
        self.g_layout.setSpacing(20)

        # 创建一个滚动区域，将水平布局添加到其中
        self.scroll_area = MyScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.g_layout)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        # 创建一个垂直布局，将滚动区域添加到其中
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.scroll_area)

        # 将垂直布局设置为主窗口的布局
        self.setLayout(self.v_layout)

        self.mouse_pos = None

    def wheelEvent(self, event):
        # 忽略滚轮事件
        event.accept()

    def mousePressEvent(self, event):
        # 记录鼠标按下时的位置
        self.mouse_pos = QtGui.QCursor.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            # 计算鼠标拖动的距离
            delta = QtGui.QCursor.pos() - self.mouse_pos

            # 计算滚动条应该滚动到的位置
            scrollbar = self.scroll_area.horizontalScrollBar()
            value = scrollbar.value() - delta.x()

            # 设置滚动条的位置
            scrollbar.setValue(value)

            # 更新鼠标位置
            self.mouse_pos = QtGui.QCursor.pos()

    def mouseReleaseEvent(self, event):
        # 清除已经记录的鼠标位置
        self.mouse_pos = None
        # 保证位置是60的整数倍
        scrollbar = self.scroll_area.horizontalScrollBar()
        value = scrollbar.value()
        scrollbar.setValue(value)
        scrollbar.setValue(round(value / 70) * 70)

# 自定义滚动控件
class MyScrollArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        # 忽略滚轮事件
        event.accept()




# 自定义按钮
class MyQPushButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_drag_flag = False
        self._drag_start_pos = None

    def mousePressEvent(self, event):
        self.mouse_drag_flag = False
        event.ignore()
        self.setDown(True)

    def mouseMoveEvent(self, event):
        self.mouse_drag_flag = True
        event.ignore()
        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mouse_drag_flag:
            event.ignore()
            self.setDown(False)
        else:
            self.click()


