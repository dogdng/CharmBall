# -*- coding: utf-8 -*-
import math
from os import cpu_count
import psutil, sys, time
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QPainter, QPalette, QFont, QColor
from pynput.mouse import Controller
from interface import Windows


class GradientColor():
    '''渐变色配色'''
    christmas = ("#FF0080", "#FF8C00", "#40E0D0") # 绿 -> 黄 -> 红
    wedding_day_blues = ("#FF0080", "#FFF200", "#1E9600") # 绿 -> 黄 -> 红
    superman = ("#F11712", "#0099F7") # 蓝 -> 红
    meridian = ("#283c86", "#45a247") # 绿 -> 蓝
    dogdng = ("#FF0020", "#338CE0", "#30E0B0")


class DashBoard(QWidget):
    '''仪表盘'''
    __value = 0
    def __init__(self, margin, line_width, parent = None) -> None:
        super(DashBoard, self).__init__(parent)
        self.__margin = margin
        self.__line_width = line_width

        # 旋转角度-绘制部分，startAngle和spanAngle必须以1/16度指定
        self.arc_angle_ratio = -1 * 270 * 16 / 100
        self.arc_start_angle = 225 * 16
        #
        self.label = QtWidgets.QLabel(self)
        self.label.raise_()
        # 设置字体和颜色
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, "#B8B6B0")
        self.label.setPalette(palette)
        # 将文本垂直和水平居中显示
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)


    def set_value(self, value):
        self.__value = value
        # self.update() 不用重复调用

    def paintEvent(self, event):
        '重绘，所有的绘制都放在这里，因为这里能拿到放在layout里面的窗口尺寸'
        size = self.size()
        self.__diameter = min(size.width(), size.height()) # 整个widget的直径
        painter = QPainter(self)
        # painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)  # 抗锯齿
        # 背景
        self.__rect = QtCore.QRectF(0, 0, self.__diameter, self.__diameter) # 整个widget的
        self.path = QtGui.QPainterPath()
        self.path.addRoundedRect(self.__rect, self.__diameter, self.__diameter)
        painter.setClipPath(self.path)
        brush = QtGui.QBrush(QColor(150, 150, 150, 20))
        painter.fillRect(self.__rect, brush)
        # 画弧形
        gradient = QtGui.QConicalGradient(self.__rect.center(), -90) # 沿圆弧方向渐变

        gradient_color = GradientColor()
        step = len(gradient_color.dogdng)
        for i in range(step):
            pos = i / (step - 1)
            gradient.setColorAt(pos, QColor(gradient_color.dogdng[i]))

        arc_pen = QtGui.QPen(QtGui.QBrush(gradient), self.__line_width, c = Qt.PenCapStyle.RoundCap)
        arc_diameter = self.__diameter - self.__margin * 2 - self.__line_width # 仪表盘画线的直径
        painter.setPen(arc_pen)
        self.__arc_rect = QtCore.QRectF(self.__margin + self.__line_width / 2, self.__margin + self.__line_width / 2, arc_diameter, arc_diameter)
        painter.drawArc(self.__arc_rect, self.arc_start_angle, round(self.__value * self.arc_angle_ratio))
        # 中心的数字
        label_pos = self.__margin + self.__line_width
        label_size = self.__diameter - (self.__margin + self.__line_width) * 2
        font = QFont("Source Code Pro", label_size//3, weight = QFont.Weight.Normal) # 最多显示3个数字
        self.label.setFont(font)
        self.label.setGeometry(label_pos, label_pos, label_size, label_size)
        self.label.setText(str(self.__value))
        painter.end()


class CPUDashBoard(QWidget):
    '''CPU仪表盘，显示逻辑核心的占用'''
    left_click_ball = QtCore.Signal(QPoint, Windows) # 信号必须放在方法外面
    alongside_trigger = QtCore.Signal()
    __system_info_update_period = 1.0 # second
    __width_screen_ratio = 0.15 # 悬浮球相对屏幕像素的比例
    __cpu_percent: list[float] = []
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.__is_window_move = True
        self.__alongside = False
        self.__alongside_windows = False
        self.info = SystemInfo()

        self.setWindowTitle("C&B")
        # 无边框，窗口置顶
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                            | Qt.WindowType.WindowStaysOnTopHint
                            # | Qt.WindowType.Window
                            # | Qt.WindowType.Popup
                            # | Qt.WindowType.Tool # 工具窗口。工具窗口通常是一个小窗口，其标题栏和装饰比通常小，通常用于工具按钮的集合。 如果有父部件，则工具窗口将始终保持在其上。
                            | Qt.WindowType.ToolTip # 表示窗口小部件是工具提示。 这在内部用于实现工具提示，没有标题栏和窗口边框。
                            )
        # 窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        ''' 尺寸和位置 '''
        screen_size = QtGui.QGuiApplication.primaryScreen().size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.__width = round(min(screen_size.width(), screen_size.height()) * self.__width_screen_ratio)
        self.origin = QPoint(round((screen_size.width() - self.__width) / 2.0), round((screen_size.height() - self.__width) / 2.0))
        self.__alongside_width = self.__width // 25

        # 鼠标手状
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 逻辑CPU显示
        cpu_count = self.info.get_cpu_count()

        # 确实显示位置，整体界面呈方形，不足一行的中间对齐
        #  ####     ####
        #  ####     ####
        #  ####     ####
        #  ####      ##

        col = math.ceil(math.sqrt(cpu_count)) # 列数
        cols = [] # 列的索引，每一列的填充顺序
        middle = math.floor((col - 1) / 2)
        if col % 2 == 0:
            for i in range(col):
                pos = middle - math.ceil(i / 2) if i % 2 == 0 else middle + math.ceil(i / 2)
                cols.append(pos)
        else:
            for i in range(col):
                pos = middle + math.ceil(i / 2) if i % 2 == 0 else middle - math.ceil(i / 2)
                cols.append(pos)
        # print(f"cpu_count: {cpu_count}, col: {col}, middle: {middle}, cols : {cols}")
        valid_pos = [] # 可用的位置，在这些位置上需要画
        for i in range(cpu_count):
            row = math.floor(i / col)
            rol = cols[math.floor(i % col)]
            valid_pos.append([row, rol])
        # print(f"valid_pos: {valid_pos}")
        # 按顺序把cpu放在显示的位置上
        dash_board_pos = sorted(valid_pos, key=(lambda x:[x[0], x[1]]), reverse = False)
        # print(f"dash_board_pos: {dash_board_pos}")

        grid = QtWidgets.QGridLayout()
        self.cpu_dash_boards: list[DashBoard] = []
        margin = (self.__width / col) / 25
        line_width = (self.__width / col) / 8
        for i in range(cpu_count):
            dash = DashBoard(margin, line_width)
            self.cpu_dash_boards.append(dash)
            grid.addWidget(dash, dash_board_pos[i][0], dash_board_pos[i][1])
        self.setLayout(grid)


        # ''' 定时更新要显示的内容 '''
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(round(self.__system_info_update_period * 1000)) # millisecond
        self.update()

    def update_system_info(self):
        try:
            self.__cpu_percent = self.info.get_percpu_percent()
            for i in range(len(self.cpu_dash_boards)):
                self.cpu_dash_boards[i].set_value(round(self.__cpu_percent[i]))
        except:
            pass
        else:
            self.update()

    def set_origin(self, origin: QPoint):
        '''设置原点：窗口中心坐标'''
        self.origin = origin
        # self.origin = QPoint(960, 540)

    def activate(self) -> None:
        # threading.Thread(target=utils.anime_WindowOpacity, args=(self,)).start()
        self.setGeometry(round(self.origin.x() - self.__width / 2.0),
                         round(self.origin.y() - self.__width / 2.0),
                         round(self.__width),
                         round(self.__width))
        self.show()

    def mousePressEvent(self, event):
        '鼠标按下'
        globalPos = self.mapToGlobal(event.position())
        if event.button() == Qt.MouseButton.LeftButton:
            self.__is_window_move = True
            self.drag_position = globalPos - self.frameGeometry().topLeft()
            self.mouse_pos = globalPos
            self.window_pos = self.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            # self.right_click_ball.emit(Windows.RIGHT, self.origin)
            self.mouse_pos = globalPos
            self.window_pos = self.pos()
        return super().mousePressEvent(event)
        # event.accept() # 将事件标记为已处理

    def mouseMoveEvent(self, event):
        '鼠标移动'
        globalPos = self.mapToGlobal(event.position())
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.__is_window_move = False
            diff = globalPos - self.mouse_pos
            new_pos = self.window_pos + diff.toPoint()
            self.move(new_pos)
            self.origin = QPoint(new_pos.x() + self.__width//2, new_pos.y() + self.__width//2)
            event.accept()

    def mouseReleaseEvent(self, event):
        '鼠标释放'
        if event.button() == Qt.MouseButton.LeftButton:
            # 若菜单已经显示则隐藏
            if self.__is_window_move: # 防止move之后还会触发
                self.left_click_ball.emit(self.origin, Windows.LEFT)
            else:
                self.drag_position = None
        elif event.button() == Qt.MouseButton.RightButton:
            sys.exit(0)
        event.accept()

    def enterEvent(self, event):
        '鼠标进入'
        pos = self.frameGeometry().topLeft()
        if self.__alongside:
            if pos.x() + self.__width >= self.screen_width:
                # 屏幕右
                self.alongside_appear(self.screen_width - self.__width, pos.y(), "right")
            elif pos.x() <= 0:
                # 屏幕左
                self.alongside_appear(0, pos.y(), "left")
            elif pos.y() <= 0:
                # 屏幕上方
                self.alongside_appear(pos.x(), 0, "up")
            event.accept()

    def alongside_appear(self, x, y, direction):
        '侧边出现'
        self.__alongside_windows = False
        # 避免来回跳，即鼠标很靠边时触发了enterEvent，球弹出来之后自己脱离了鼠标，在这个区域会来回跳
        if direction == 'right':
            self.setGeometry(x + self.__alongside_width, y, self.__width, self.__width)
        elif direction == 'left':
            self.setGeometry(x - self.__alongside_width, y, self.__width, self.__width)
        else:
            self.setGeometry(x, y - self.__alongside_width, self.__width, self.__width)
        self.update()
        # self.__mouse_controller.position = (x + self.__ball_radius, y + self.__ball_radius * 1.35)
        self.__alongside = False

    def leaveEvent(self, event):
        '鼠标移走'
        pos = self.frameGeometry().topLeft()
        if not self.__alongside:
            if pos.x() + self.__width >= self.screen_width:
                self.alongside_disappear(self.screen_width - self.__alongside_width, pos.y(), 'right')
            elif pos.x() <= 0:
                self.alongside_disappear(self.__alongside_width - self.__width, pos.y(), 'left')
            elif pos.y() <= 0:
                self.alongside_disappear(pos.x(), self.__alongside_width - self.__width, 'up')
        # 防止被任务栏遮住
        if pos.y() + self.__width >= self.screen_height:
            self.setGeometry(pos.x(), self.screen_height - self.__width, self.__width, self.__width)
            self.__alongside = False
            self.__alongside_windows = False
        event.accept()

    def alongside_disappear(self, x, y, direction):
        '侧边贴边'
        self.__alongside = True
        self.__alongside_windows = True
        num = len(QApplication.screens())
        if direction == 'right':
            self.setGeometry(x, y, self.__alongside_width, self.__width)
        elif direction == 'left':
            # 防止跨屏
            if num < 2:
                self.setGeometry(x, y, self.__width, self.__width)
            else:
                self.setGeometry(0, y, self.__alongside_width, self.__width)
        else:
            if num < 2:
                self.setGeometry(x, y, self.__width, self.__width)
            else:
                self.setGeometry(x, 0, self.__width, self.__alongside_width)
        self.update()


    def paintEvent(self, event):
        '重绘'
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)  # 抗锯齿
        # 背景
        brush = QtGui.QBrush(QColor(0, 0, 0, 1)) # 不能全透明。全透明时，贴边唤醒会一直跳。
        if self.__alongside_windows:
            brush.setColor(QColor(0, 153, 247, 75))
            painter.fillRect(self.rect(), brush)
        else:
            painter.fillRect(self.rect(), brush)
            # 外圈弧形
            # self.dash_board.update()
        painter.end()

class SystemInfo(object):
    def __init__(self) -> None:
        pass

    def get_cpu_count(self):
        return psutil.cpu_count(logical=True)

    def get_percpu_percent(self):
        return psutil.cpu_percent(interval = 0, percpu=True)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    test = CPUDashBoard(app)
    test.activate()
    sys.exit(app.exec())