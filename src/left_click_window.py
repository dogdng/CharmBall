# -*- coding: utf-8 -*-

import os, PySide6
import sys, threading
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *



class LeftClickWindow(QWidget):
    '''
    单击功能窗口
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window B")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window | Qt.Tool
        )

        window_b_width = 202
        window_b_height = 498
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setGeometry(200, 200, window_b_width, window_b_height)
        self.setWindowOpacity(0.9)

        self.add_buttons()

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

        self.button2 = MyQPushButton(self)
        self.button2.setIcon(QIcon("./resources/flash.png"))
        self.button2.setIconSize(QSize(50, 50))
        self.button2.setFixedSize(50, 50)
        self.button2.clicked.connect(self.open_quicker)
        self.scroll1.g_layout.addWidget(self.button2, 0, 1)
        self.button2.setStyleSheet(button_style)

        self.button3 = MyQPushButton(self)
        self.button3.setIcon(QIcon("./resources/screen.png"))
        self.button3.setIconSize(QSize(50, 50))
        self.button3.setFixedSize(50, 50)
        self.button3.clicked.connect(self.change_screen)
        self.scroll1.g_layout.addWidget(self.button3, 0, 2)
        self.button3.setStyleSheet(button_style)

        self.button5 = MyQPushButton(self)
        self.button5.setIcon(QIcon("./resources/closemenu.png"))
        self.button5.setIconSize(QSize(50, 50))
        self.button5.setFixedSize(50, 50)
        self.button5.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.button5, 0, 3)
        self.button5.setStyleSheet(button_style)

        self.button52 = MyQPushButton(self)
        self.button52.setIcon(QIcon("./resources/closemenu.png"))
        self.button52.setIconSize(QSize(50, 50))
        self.button52.setFixedSize(50, 50)
        self.button52.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.button52, 0, 4)
        self.button52.setStyleSheet(button_style)

        self.button53 = MyQPushButton(self)
        self.button53.setIcon(QIcon("./resources/closemenu.png"))
        self.button53.setIconSize(QSize(50, 50))
        self.button53.setFixedSize(50, 50)
        self.button53.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.button53, 0, 5)
        self.button53.setStyleSheet(button_style)

        self.button54 = MyQPushButton(self)
        self.button54.setIcon(QIcon("./resources/closemenu.png"))
        self.button54.setIconSize(QSize(50, 50))
        self.button54.setFixedSize(50, 50)
        self.button54.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.button54, 0, 6)
        self.button54.setStyleSheet(button_style)

        self.button55 = MyQPushButton(self)
        self.button55.setIcon(QIcon("./resources/closemenu.png"))
        self.button55.setIconSize(QSize(50, 50))
        self.button55.setFixedSize(50, 50)
        self.button55.clicked.connect(self.switch_to_window_a)
        self.scroll1.g_layout.addWidget(self.button55, 0, 7)
        self.button55.setStyleSheet(button_style)

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
        layout.setAlignment(Qt.AlignCenter)
        # 将布局应用到父控件
        self.setLayout(layout)

    """
    鼠标事件
    """

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = None
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_flag = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            # 范围判定用
            self.mouse_pos = event.globalPos()
            self.window_pos = self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        global app
        # print(self.width(),self.height())
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.mouse_flag = False

            # 获取焦点屏幕
            focus_screen = get_focus_screen()
            # 获取焦点屏幕的参数
            f_screen_geometry = focus_screen.geometry()
            f_x, f_y, f_width, f_height = (
                f_screen_geometry.x(),
                f_screen_geometry.y(),
                f_screen_geometry.width(),
                f_screen_geometry.height(),
            )
            f_scale_factor = focus_screen.devicePixelRatio()
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

    """
    重绘
    """

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 设置画笔避免边缘黑色
        painter.setPen(Qt.NoPen)
        # Draw rounded rectangle
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 25, 25)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QBrush(QColor("#28323B")))

    """
    按钮槽函数
    """
    def switch_to_window_a(self):
        global main
        # print(self.rect())
        self.hide()
        self.window_a = main
        self.window_a.tray_flag = True

        self.window_a.setGeometry(
            self.geometry().center().x() - self.window_a.width() / 2,
            self.geometry().center().y() - self.window_a.height() / 2,
            main_window_width,
            window_a_height,
        )

        threading.Thread(target=anime_WindowOpacity, args=(self.window_a,)).start()

        self.window_a.show()

    def mission_view(self):
        pyautogui.hotkey("winleft", "tab")

    def open_taskmgr(self):
        pyautogui.hotkey("ctrl", "shift", "esc")

    def open_quicker(self):
        hwnd = win32gui.FindWindow(0, "Quicker面板窗口")

        if hwnd != 0:
            self.hide()
            focus_screen = get_focus_screen()
            # 获取焦点屏幕的参数
            f_screen_geometry = focus_screen.geometry()
            # 这里需要获取主屏幕的缩放系数，这个函数恰好只能获取主屏幕的，正好用这个
            f_scale_factor = focus_screen.devicePixelRatio()

            # 这个的输入是未缩放坐标
            # 这个关系是缩放坐标到未缩放坐标的变换关系
            pyautogui.middleClick(
                x=f_screen_geometry.left()
                + (self.geometry().center().x() - f_screen_geometry.left())
                * f_scale_factor,
                y=f_screen_geometry.top()
                + (self.geometry().center().y() - f_screen_geometry.top())
                * f_scale_factor,
            )

            # win32gui.ShowWindow(hwnd,win32con.SW_SHOW)

            # 判断窗口是否可见
            # 本来判断了这个win32gui.IsWindowVisible(hwnd)，会导致不能短时间响应
            if True:
                # print("================================================")
                # time.sleep(0.1)
                while win32gui.IsWindowVisible(hwnd):
                    pass
                # 获取窗口位置和大小, 这里返回的是未经缩放的坐标
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)

                # 计算缩放后的宽度和高度
                # width = (right - left)
                # height = (bottom - top)
                width = (right - left) / f_scale_factor
                height = (bottom - top) / f_scale_factor

                # 此处的0.44是quicker窗口的上面部分的高度，目前无法直接通过win32api获取到这个高度，因此测量了比例为0.44
                # 这个变换
                # 如存在问题，修改主显示器
                time.sleep(0.1)
                self.move(
                    f_screen_geometry.left()
                    + (left - f_screen_geometry.left()) / f_scale_factor
                    + width / 2
                    - self.width() / 2,
                    f_screen_geometry.top()
                    + (top - f_screen_geometry.top()) / f_scale_factor
                    + height * 0.44
                    - self.height() / 2,
                )

                # QT坐标为缩放坐标，WIN32坐标为未缩放坐标，把设计WIN32坐标的操作全用win32api完成就没问题了
                # 获取本窗口句柄
                # time.sleep(0.1)
                # hwnd = self.winId()
                # win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, int(left+width/2-self.width()/2),
                #                     int(top+height/2-self.height()/2), self.width(), self.height(), win32con.SWP_SHOWWINDOW)

                threading.Thread(target=anime_WindowOpacity, args=(self,)).start()
                self.show()
            else:
                pass

    def change_screen(self):
        global app
        # 首先判断焦点屏幕
        screens = app.screens()
        # 判断激活的屏幕的序号
        for index, screen in enumerate(screens):
            screen_geometry = screen.geometry()
            x, y, width, height = (
                screen_geometry.x(),
                screen_geometry.y(),
                screen_geometry.width(),
                screen_geometry.height(),
            )
            scale_factor = screen.devicePixelRatio()
            cursor_pos = QCursor.pos()
            # 判断鼠标在不在该屏幕内
            if (
                x <= cursor_pos.x() < x + width * scale_factor
                and y <= cursor_pos.y() < y + height * scale_factor
            ):
                break

        num_screens = len(screens) - 1

        if index + 1 > num_screens:
            index = 0
        else:
            index += 1

        # 将下一块屏幕取出
        to_screen = screens.pop(index)

        # 获取焦点屏幕的参数
        to_screen_geometry = to_screen.geometry()
        f_x, f_y, f_width, f_height = (
            to_screen_geometry.x(),
            to_screen_geometry.y(),
            to_screen_geometry.width(),
            to_screen_geometry.height(),
        )

        f_xrb = round(f_x + f_width)
        f_yrb = round(f_y + f_height)

        self.move(
            (f_x + f_xrb) / 2 - self.width() / 2, (f_y + f_yrb) / 2 - self.height() / 2
        )

    def back_desktop(self):
        pyautogui.hotkey("winleft", "d")

    def open_utools(self):
        pyautogui.hotkey("alt", "space")
        subprocess.Popen("TabTip")

    def take_screenshot(self):
        # 模拟按下win+shift+s
        pyautogui.hotkey("winleft", "shift", "s")
        # 创建新线程等待0.5秒后显示窗口
        t = threading.Timer(1.0, self.show)
        t.start()
        # 隐藏悬浮球窗口
        self.hide()



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
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.g_layout)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        self.g_layout = QGridLayout()
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

# 自定义滚动控件
class MyScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        # 忽略滚轮事件
        event.accept()


# Slider类
class CircularSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setRange(0, 360)  # 设置范围
        self.setSingleStep(1)  # 设置步长
        self.setPageStep(15)  # 设置页面步长

        self.setValue(66)

        # 设置标签
        self.label = QLabel(self)
        self.label.raise_()
        # 设置字体和颜色
        font = QFont("Comic Sans MS", 60, QFont.Bold)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.red)
        palette = QPalette()

        self.label.setFont(font)
        self.label.setPalette(palette)
        # 将文本垂直和水平居中显示
        self.label.setAlignment(Qt.AlignCenter)

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
        palette = QPalette()
        r = 40 + int((145 - 40) * temp_val / 100)
        g = 50 + int((150 - 50) * temp_val / 100)
        b = 59 + int((156 - 59) * temp_val / 100)
        color = QColor(r, g, b)
        palette.setColor(QPalette.WindowText, color)
        self.label.setPalette(palette)
        # 更新标签的文本为滑块的值
        self.label.setText("{}".format(temp_val))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        width = self.width()
        height = self.height()
        rect_size = min(width, height)
        rect = QRectF(
            (width - rect_size) / 2, (height - rect_size) / 2, rect_size, rect_size
        )

        # 绘制背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(rect)

        # 绘制弧形
        center = rect.center()
        gradient = QConicalGradient(center, -270)
        gradient.setColorAt(0, QColor(145, 150, 156))
        # gradient.setColorAt(0.5, QColor(255, 255, 0))
        gradient.setColorAt(1, QColor(40, 50, 59))
        painter.setBrush(QBrush(gradient))
        # startAngle和spanAngle必须以1/16度指定

        pen = QPen(QBrush(gradient), 30)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        rect_size = min(width, height) - 50
        rect = QRectF(
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
                pyautogui.press("playpause")
        else:
            pass
        self.mouse_event_flag = 2
        self.mouse_drag_flag = False

    def angle(self, event):
        self.last_angle = self.value()
        center = self.rect().center()
        x = event.pos().x() - center.x()
        y = event.pos().y() - center.y()
        ag = round((180 / 3.14159 * (atan2(y, x))) % 360)
        if 315 > ag > 225:
            ag = self.last_angle
        return ag


# 自定义按钮
class MyQPushButton(QPushButton):
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


