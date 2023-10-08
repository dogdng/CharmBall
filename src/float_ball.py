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
    __system_info_update_period = 1 # second
    __ball_radius_screen_ratio = 0.05
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


        '''
        外部大扇形环 内存使用
        '''
        #
        # 背景
        self.path = QtGui.QPainterPath()
        self.path.addRoundedRect(self.rect(), self.__ball_radius, self.__ball_radius)
        # 弧形条
        gradient = QtGui.QConicalGradient(self.rect().center(), -90)
        # Wedding Day Blues 绿 -> 黄 -> 红
        # gradient.setColorAt(0, QColor("#FF0080"))
        # gradient.setColorAt(0.5, QColor("#FFF200"))
        # gradient.setColorAt(1, QColor("#1E9600"))

        # Christmas 绿 -> 黄 -> 红
        gradient.setColorAt(0, QColor("#FF0080"))
        gradient.setColorAt(0.5, QColor("#FF8C00"))
        gradient.setColorAt(1, QColor("#40E0D0"))

        # Superman 蓝 -> 红
        # gradient.setColorAt(0, QColor("#F11712"))
        # gradient.setColorAt(1, QColor("#0099F7"))

        # Meridian 绿 -> 蓝
        # gradient.setColorAt(0, QColor("#283c86"))
        # gradient.setColorAt(1, QColor("#45a247"))
        self.arc_start_angle = 225 * 16
        self.memory_arc_angle_ratio = -1 * 270 * 16 / 100
        memory_arc_width = self.__ball_radius / 5
        self.pen = QtGui.QPen(QtGui.QBrush(gradient), memory_arc_width, c = Qt.PenCapStyle.RoundCap)
        memory_arc_margin = self.__ball_radius / 6
        memory_arc_diameter = (self.__ball_radius - memory_arc_margin) * 2
        self.memory_arc_rect = QtCore.QRectF(
            (self.width() - memory_arc_diameter) / 2, (self.height() - memory_arc_diameter) / 2, memory_arc_diameter, memory_arc_diameter
        )

        '''
        中心标签 网速
        '''
        [self.sent_history, self.recv_history] = self.info.get_net_speed()
        # 设置标签
        self.label = QtWidgets.QLabel(self)
        self.label.raise_()
        # 设置字体和颜色
        font = QFont("Comic Sans MS", self.__ball_radius//5, QFont.Weight.Bold)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.red)
        palette = QPalette()
        self.label.setFont(font)

        r = 255 # 40 + int((145 - 40) * 67 / 100)
        g = 0 # 50 + int((150 - 50) * 67 / 100)
        b = 0 # 59 + int((156 - 59) * 67 / 100)
        color = QColor(r, g, b)
        palette.setColor(QPalette.ColorRole.WindowText, color)
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
        self.__memory_percent = self.info.get_memory_percent()
        # self.memory_percent = self.memory_percent + 5 if self.memory_percent < 100 else 0
        [sent_now, recv_now] = self.info.get_net_speed()
        sent = (sent_now - self.sent_history)/1024/self.__system_info_update_period  # 算出1秒后的差值
        recv = (recv_now - self.recv_history)/1024/self.__system_info_update_period
        self.sent_history = sent_now
        self.recv_history = recv_now
        self.__net_speed = "↑:{0:>3.1f}K\n↓:{1:>3.1f}K".format(sent, recv)
        self.update()

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
        painter.setClipPath(self.path)
        painter.fillRect(self.rect(), QtGui.QBrush(QColor(150, 150, 150, 20)))
        # 外圈弧形
        painter.setPen(self.pen)
        # 限制旋转角度-绘制部分，startAngle和spanAngle必须以1/16度指定
        painter.drawArc(self.memory_arc_rect, self.arc_start_angle, round(self.__memory_percent * self.memory_arc_angle_ratio))

        self.label.setText(self.__net_speed)

        painter.end()


class SystemInfo(object):
    def __init__(self) -> None:
        while False:
            cup_per = psutil.cpu_percent(interval = 1, percpu=False)  # 此时刷新时间是5秒
            # 内存信息
            memory_info = psutil.virtual_memory()
            # 硬盘信息
            disk_info = psutil.disk_usage("/")  # 根目录磁盘信息
            # 网络信息
            net_info = psutil.net_io_counters()
            # 拼接显示
            log_str = "|----------|----------|----------|\n"
            log_str += "|----cpu----|--memory--|---disk---|\n"
            log_str += "|     %d     |   %.2fG  |  %.2f  |\n" % (
            psutil.cpu_count(logical=True), memory_info.total / 1024 / 1024 / 1024, disk_info.total / 1024 / 1024 / 1024)
            log_str += "|  %s%%  |   %s%%  |   %s%%  |\n" % (
            cup_per, memory_info.percent, disk_info.percent)
            print(log_str)
            sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
            recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
            sleep(1)
            sent_now = psutil.net_io_counters().bytes_sent
            recv_now = psutil.net_io_counters().bytes_recv
            sent = (sent_now - sent_before)/1024  # 算出1秒后的差值
            recv = (recv_now - recv_before)/1024
            print("上传：{0}KB/s".format("%.2f"%sent))
            print("下载：{0}KB/s".format("%.2f"%recv))
            print('-'*32)
            sleep(2)
    def get_cpu_percent(self):
        return psutil.cpu_percent(interval = 0, percpu=False)

    def get_memory_percent(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent

    def get_net_speed(self):
        sent = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv = psutil.net_io_counters().bytes_recv  # 已接收的流量
        return [sent, recv]
