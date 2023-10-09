# -*- coding: utf-8 -*-
import os, psutil, sys, threading, time
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QPainter, QPalette, QFont, QColor

import utils
from interface import Windows

class FloatBall(QWidget):
    click_ball = QtCore.Signal(Windows, QPoint) # 信号必须放在方法外面
    __ball_radius : int
    __memory_percent = 0.0
    __cpu_percent = 0.0
    __system_info_update_period = 1 # second
    __ball_radius_screen_ratio = 0.05 # 悬浮球相对屏幕像素的比例
    __net_speed = ""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.info = SystemInfo()

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
        self.__ball_radius = round(min(screen_size.width(), screen_size.height()) * self.__ball_radius_screen_ratio)
        self.window_size = QSize(self.__ball_radius * 2, self.__ball_radius * 2)
        self.origin = QPoint(screen_size.width()//2 - self.__ball_radius, screen_size.height()//2 - self.__ball_radius)
        self.setGeometry(self.origin.x() - self.__ball_radius, self.origin.y() - self.__ball_radius, self.window_size.width(), self.window_size.height())

        # 设置透明度
        # self.setWindowOpacity(0.9)
        # 鼠标手状
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_window_move = True


        # 背景
        self.path = QtGui.QPainterPath()
        self.path.addRoundedRect(self.rect(), self.__ball_radius, self.__ball_radius)
        self.arc_start_angle = 225 * 16
        '''
        外部大扇形环 内存使用
        '''
        # 弧形条
        memory_gradient = QtGui.QConicalGradient(self.rect().center(), -90)
        # Wedding Day Blues 绿 -> 黄 -> 红
        # gradient.setColorAt(0, QColor("#FF0080"))
        # gradient.setColorAt(0.5, QColor("#FFF200"))
        # gradient.setColorAt(1, QColor("#1E9600"))

        # Christmas 绿 -> 黄 -> 红
        # memory_gradient.setColorAt(0, QColor("#FF0080"))
        # memory_gradient.setColorAt(0.5, QColor("#FF8C00"))
        # memory_gradient.setColorAt(1, QColor("#40E0D0"))

        memory_gradient.setColorAt(0, QColor("#FF0020"))
        memory_gradient.setColorAt(0.5, QColor("#338CE0"))
        memory_gradient.setColorAt(1, QColor("#30E0B0"))

        # Superman 蓝 -> 红
        # gradient.setColorAt(0, QColor("#F11712"))
        # gradient.setColorAt(1, QColor("#0099F7"))

        # Meridian 绿 -> 蓝
        # gradient.setColorAt(0, QColor("#283c86"))
        # gradient.setColorAt(1, QColor("#45a247"))

        # 旋转角度-绘制部分，startAngle和spanAngle必须以1/16度指定
        self.arc_angle_ratio = -1 * 270 * 16 / 100
        memory_arc_width = self.__ball_radius / 5
        self.memory_pen = QtGui.QPen(QtGui.QBrush(memory_gradient), memory_arc_width, c = Qt.PenCapStyle.RoundCap)
        memory_arc_margin = self.__ball_radius / 6
        memory_arc_diameter = (self.__ball_radius - memory_arc_margin) * 2
        self.memory_arc_rect = QtCore.QRectF(
            (self.width() - memory_arc_diameter) / 2, (self.height() - memory_arc_diameter) / 2, memory_arc_diameter, memory_arc_diameter
        )

        '''
        底部小扇形环 CPU使用
        r = R / (sqrt(2) + 1)
        sqrt(2) + 1 取 2.4
        为了不挤到中间的label，再缩小2倍
        '''
        cpu_arc_diameter = memory_arc_diameter / 4
        center = QPoint(round(self.width() / 2), round((self.height() + memory_arc_diameter) / 2))
        # 弧形条
        cpu_gradient = QtGui.QConicalGradient(center, -90)

        # Superman 蓝 -> 红
        cpu_gradient.setColorAt(0, QColor("#F11712"))
        cpu_gradient.setColorAt(1, QColor("#0099F7"))

        cpu_arc_width = self.__ball_radius / 10
        self.cpu_pen = QtGui.QPen(QtGui.QBrush(cpu_gradient), cpu_arc_width, c = Qt.PenCapStyle.MPenCapStyle)
        self.cpu_arc_rect = QtCore.QRectF(
            (self.width() - cpu_arc_diameter) / 2, (self.height() + memory_arc_diameter) / 2 - cpu_arc_diameter, cpu_arc_diameter, cpu_arc_diameter
        )

        '''
        中心标签 网速
        '''
        [self.sent_history, self.recv_history] = self.info.get_net_speed()
        # 设置标签
        self.label = QtWidgets.QLabel(self)
        self.label.raise_()
        # 设置字体和颜色
        font = QFont("Source Code Pro", round(self.__ball_radius/5.5), QFont.Weight.Normal)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.red)
        palette = QPalette()
        self.label.setFont(font)

        palette.setColor(QPalette.ColorRole.WindowText, "#CCCCCC")
        self.label.setPalette(palette)
        # 将文本垂直和水平居中显示
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.label.setGeometry(self.__ball_radius//2, self.__ball_radius//2, self.__ball_radius, self.__ball_radius)
        '''
        定时更新要显示的内容
        '''
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(self.__system_info_update_period * 1000) # millisecond

    def update_system_info(self):
        # 内存占用
        self.__memory_percent = self.info.get_memory_percent()
        # self.__memory_percent = self.__memory_percent + 5 if self.__memory_percent < 100 else 0
        # CPU占用
        self.__cpu_percent = self.info.get_cpu_percent()
        # self.__cpu_percent = self.__cpu_percent + 5 if self.__cpu_percent < 100 else 0
        # 网速
        [sent_now, recv_now] = self.info.get_net_speed()
        sent = (sent_now - self.sent_history)/1024/self.__system_info_update_period  # 算出1秒后的差值
        recv = (recv_now - self.recv_history)/1024/self.__system_info_update_period
        self.sent_history = sent_now
        self.recv_history = recv_now
        self.__net_speed = "↑:{0}\n↓:{1}".format(self.net_speed_format(sent), self.net_speed_format(recv))
        self.net_speed_format(recv_now)
        self.update()

    def net_speed_format(self, speed: float) -> str:
        result = ""
        if speed < 10.0:
            result = "{0:>.2f}K".format(speed)
        elif speed < 100.0:
            result = "{0:>.1f}K".format(speed)
        elif speed < 1000.0:
            result = "{0:>.0f}.K".format(speed)
        elif speed < 10000.0:
            result = "{0:>.2f}M".format(speed/1000.0)
        elif speed < 100000.0:
            result = "{0:>.1f}M".format(speed/1000.0)
        elif speed < 1000000.0:
            result = "{0:>.0f}.M".format(speed/1000.0)
        elif speed < 10000000.0:
            result = "{0:>.2f}G".format(speed/1000000.0)
        else: # May be enough at 2023
            result = "{0:>.1f}G".format(speed/1000000.0)
        return result

    def set_origin(self, origin: QPoint):
        '''设置原点：窗口中心坐标'''
        self.origin = origin
        # self.origin = QPoint(960, 540)

    def activate(self) -> None:
        # threading.Thread(target=utils.anime_WindowOpacity, args=(self,)).start()
        self.setGeometry(self.origin.x() - self.__ball_radius, self.origin.y() - self.__ball_radius, self.window_size.width(), self.window_size.height())
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
            self.origin = QPoint(new_pos.x() + self.__ball_radius, new_pos.y() + self.__ball_radius)
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

    def paintEvent(self, event):
        '重绘'
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)  # 抗锯齿
        # 背景
        painter.setClipPath(self.path)
        painter.fillRect(self.rect(), QtGui.QBrush(QColor(150, 150, 150, 20)))
        # 外圈弧形
        painter.setPen(self.memory_pen)
        painter.drawArc(self.memory_arc_rect, self.arc_start_angle, round(self.__memory_percent * self.arc_angle_ratio))
        # 底部弧形
        painter.setPen(self.cpu_pen)
        painter.drawArc(self.cpu_arc_rect, self.arc_start_angle, round(self.__cpu_percent * self.arc_angle_ratio))
        # 中心的网速label
        self.label.setText(self.__net_speed)

        painter.end()


class SystemInfo(object):
    def __init__(self) -> None:
        pass

    def get_cpu_percent(self):
        return psutil.cpu_percent(interval = 0, percpu=False)

    def get_memory_percent(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent

    def get_net_speed(self):
        sent = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv = psutil.net_io_counters().bytes_recv  # 已接收的流量
        return [sent, recv]
