# -*- coding: utf-8 -*-

import sys, threading, math
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout

import utils, interface



class LeftClickWindow(QWidget):
    '''
    单击功能窗口
    '''
    switch_ball = QtCore.Signal(interface.Windows, QPoint) # 信号必须放在方法外面
    origin = QPoint()
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Window B")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Window | Qt.WindowType.Tool)

        # self.origin
        self.window_size = QSize(202, 498)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setGeometry(self.origin.x() - round(self.window_size.width()/2), self.origin.y() - round(self.window_size.height()/2), self.window_size.width(), self.window_size.height())
        self.setWindowOpacity(0.9)

        self.add_buttons()

    def set_origin(self, origin: QPoint):
        '''设置原点：窗口中心坐标'''
        self.origin = origin

    def add_buttons(self):
        # 设置布局

        # 一个垂直布局，第一层、第三层套两个网格布局，第二层放Slider

        layout = QVBoxLayout()
        # 设置布局为垂直居中对齐
        layout.setAlignment(Qt.AlignVCenter)
        # 将布局应用到父控件
        self.setLayout(layout)

        self.scroll1 = ScrollableButtonGrid()
        # self.scroll1.resize(300,20)

        self.scroll2 = ScrollableButtonGrid()
        # self.scroll2.resize(300,20)

        self.layout().addWidget(self.scroll1)

        self.slider = CircularSlider()
        self.slider.setFixedSize(300, 300)
        self.layout().addWidget(self.slider)

        self.layout().addWidget(self.scroll2)

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
        self.button1.setIcon(QIcon("./resources/mission.png"))
        self.button1.setIconSize(QSize(50, 50))
        self.button1.setFixedSize(50, 50)
        self.button1.clicked.connect(self.mission_view)
        self.scroll1.g_layout.addWidget(self.button1, 0, 0)
        self.button1.setStyleSheet(button_style)

        self.button3 = MyQPushButton(self)
        self.button3.setIcon(QIcon("./resources/screen.png"))
        self.button3.setIconSize(QSize(50, 50))
        self.button3.setFixedSize(50, 50)
        self.button3.clicked.connect(self.change_screen)
        self.scroll1.g_layout.addWidget(self.button3, 0, 2)
        self.button3.setStyleSheet(button_style)

        self.close_button = MyQPushButton(self)
        self.close_button.setIcon(QIcon("./resources/closemenu.png"))
        self.close_button.setIconSize(QSize(50, 50))
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.close_button, 0, 3)
        self.close_button.setStyleSheet(button_style)

        self.button6 = MyQPushButton(self)
        self.button6.setIcon(QIcon("./resources/desktop.png"))
        self.button6.setIconSize(QSize(50, 50))
        self.button6.setFixedSize(50, 50)
        self.button6.clicked.connect(self.back_desktop)
        self.scroll2.g_layout.addWidget(self.button6, 0, 0)
        self.button6.setStyleSheet(button_style)

        self.button7 = MyQPushButton(self)
        self.button7.setIcon(QIcon("./resources/taskmgr.png"))
        self.button7.setIconSize(QSize(50, 50))
        self.button7.setFixedSize(50, 50)
        self.button7.clicked.connect(self.open_taskmgr)
        self.scroll2.g_layout.addWidget(self.button7, 0, 1)
        self.button7.setStyleSheet(button_style)

        self.button8 = MyQPushButton(self)
        self.button8.setIcon(QIcon("./resources/utools.png"))
        self.button8.setIconSize(QSize(45, 45))
        self.button8.setFixedSize(50, 50)
        self.button8.clicked.connect(self.open_utools)
        self.scroll2.g_layout.addWidget(self.button8, 0, 2)
        self.button8.setStyleSheet(button_style)

        self.button9 = MyQPushButton(self)
        self.button9.setIcon(QIcon("./resources/screenshot.png"))
        self.button9.setIconSize(QSize(50, 50))
        self.button9.setFixedSize(50, 50)
        self.button9.clicked.connect(self.take_screenshot)
        self.scroll2.g_layout.addWidget(self.button9, 0, 3)
        self.button9.setStyleSheet(button_style)

        self.button91 = MyQPushButton(self)
        self.button91.setIcon(QIcon("./resources/screenshot.png"))
        self.button91.setIconSize(QSize(50, 50))
        self.button91.setFixedSize(50, 50)
        self.button91.clicked.connect(self.take_screenshot)
        self.scroll2.g_layout.addWidget(self.button91, 0, 4)
        self.button91.setStyleSheet(button_style)

        self.button92 = MyQPushButton(self)
        self.button92.setIcon(QIcon("./resources/screenshot.png"))
        self.button92.setIconSize(QSize(50, 50))
        self.button92.setFixedSize(50, 50)
        self.button92.clicked.connect(self.take_screenshot)
        self.scroll2.g_layout.addWidget(self.button92, 0, 5)
        self.button92.setStyleSheet(button_style)

        # 设置布局为垂直居中对齐
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 将布局应用到父控件
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
            event.accept()

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
    def switch_to_window_a(self):
        self.switch_ball.emit(interface.Windows.BALL, self.origin)

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
    def __init__(self):
        super().__init__()

        # 创建一个网格布局，用于添加按钮
        self.g_layout = QGridLayout()
        self.g_layout.setSpacing(20)

        # 创建一个滚动区域，将水平布局添加到其中
        self.scroll_area = MyScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtWidgets.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.g_layout)

        self.scroll_area.setVerticalScrollBarPolicy(QtWidgets.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(QtWidgets.Qt.ScrollBarAlwaysOff)
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
        self.mouse_pos = QtWidgets.QCursor.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            # 计算鼠标拖动的距离
            delta = QtWidgets.QCursor.pos() - self.mouse_pos

            # 计算滚动条应该滚动到的位置
            scrollbar = self.scroll_area.horizontalScrollBar()
            value = scrollbar.value() - delta.x()

            # 设置滚动条的位置
            scrollbar.setValue(value)

            # 更新鼠标位置
            self.mouse_pos = QtWidgets.QCursor.pos()

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


# Slider类
class CircularSlider(QtWidgets.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setRange(0, 360)  # 设置范围
        self.setSingleStep(1)  # 设置步长
        self.setPageStep(15)  # 设置页面步长

        self.setValue(66)

        # 设置标签
        self.label = QtWidgets.QLabel(self)
        self.label.raise_()
        # 设置字体和颜色
        font = QtGui.QFont("Comic Sans MS", 60, QtGui.QFont.Bold)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.Qt.red)
        palette = QtGui.QPalette()

        self.label.setFont(font)
        self.label.setPalette(palette)
        # 将文本垂直和水平居中显示
        self.label.setAlignment(QtGui.Qt.AlignCenter)

        # 将滑块的 valueChanged 信号连接到更新标签的槽函数
        self.valueChanged.connect(self.updateLabel)

        # 上一次鼠标事件发生在音量调节范围以内，则为0
        # 上一次鼠标事件发生在音量调节范围外，则为1
        # 每次鼠标释放事件后重新置为2
        self.mouse_event_flag = 2

        # 鼠标点击后是否拖动标志位，True则未发生拖动
        self.mouse_drag_flag = False

    def updateLabel(self, value):
        # 根据音量更新标签字体颜色
        temp_val = round(self.vol)
        palette = QtGui.QPalette()
        r = 40 + int((145 - 40) * temp_val / 100)
        g = 50 + int((150 - 50) * temp_val / 100)
        b = 59 + int((156 - 59) * temp_val / 100)
        color = QtGui.QColor(r, g, b)
        palette.setColor(QtGui.QPalette.WindowText, color)
        self.label.setPalette(palette)
        # 更新标签的文本为滑块的值
        self.label.setText("{}".format(temp_val))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        width = self.width()
        height = self.height()
        rect_size = min(width, height)
        rect = QtCore.QRectF(
            (width - rect_size) / 2, (height - rect_size) / 2, rect_size, rect_size
        )

        # 绘制背景
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(rect)

        # 绘制弧形
        center = rect.center()
        gradient = QtGui.QConicalGradient(center, -270)
        gradient.setColorAt(0, QtGui.QColor(145, 150, 156))
        # gradient.setColorAt(0.5, QColor(255, 255, 0))
        gradient.setColorAt(1, QtGui.QColor(40, 50, 59))
        painter.setBrush(QtGui.QBrush(gradient))
        # startAngle和spanAngle必须以1/16度指定

        pen = QtGui.QPen(QtGui.QBrush(gradient), 30)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        rect_size = min(width, height) - 50
        rect = QtCore.QRectF(
            (width - rect_size) / 2, (height - rect_size) / 2, rect_size, rect_size
        )

        # 限制旋转角度-绘制部分
        if -self.value() * 16 < -270 * 16:
            painter.drawArc(rect, 45 * 16, -self.value() * 16 + 315 * 16)
        else:
            painter.drawArc(rect, 45 * 16, -self.value() * 16 - 45 * 16)

        # 因为重绘有控件大小改变，所以在这里重新设置标签大小位置
        self.label.setGeometry(
            self.width() / 2 - 150 / 2, self.height() / 2 - 150 / 2, 150, 150
        )

    def mousePressEvent(self, event):
        # 若未鼠标事件未发生在靠近滑动条的位置，则该事件忽略，上报父窗口，实现拖动窗口
        center = self.rect().center()
        x = event.pos().x() - center.x()
        y = event.pos().y() - center.y()
        # print(sqrt(x**2+y**2))
        if 150**2 >= x**2 + y**2 >= (102) ** 2:
            self.setValue(self.angle(event))
            self.mouse_event_flag = 0
        else:
            self.mouse_event_flag = 1
            event.ignore()
            self.parent().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.mouse_drag_flag = True
        if self.mouse_event_flag == 1:
            event.ignore()
            self.parent().mousePressEvent(event)
        else:
            self.setValue(self.angle(event))
            if self.value() >= 315:
                self.vol = (self.value() - 315) / 270 * 100
            else:
                self.vol = (self.value() + 45) / 270 * 100
            # set_system_volume(self.vol)

    def mouseReleaseEvent(self, event):
        if self.mouse_event_flag == 1:
            event.ignore()
            self.parent().mousePressEvent(event)
            if not self.mouse_drag_flag:
                pass # pyautogui.press("playpause")
        else:
            pass
        self.mouse_event_flag = 2
        self.mouse_drag_flag = False

    def angle(self, event):
        self.last_angle = self.value()
        center = self.rect().center()
        x = event.pos().x() - center.x()
        y = event.pos().y() - center.y()
        ag = round((180 / 3.14159 * (math.atan2(y, x))) % 360)
        if 315 > ag > 225:
            ag = self.last_angle
        return ag


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


