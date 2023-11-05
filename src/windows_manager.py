# -*- coding: utf-8 -*-

import os, PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PySide6 import QtGui, QtWidgets, QtCore

from interface import Windows
import utils
from tray_button import TrayButton
from float_ball import FloatBall
from matrix_menu import MatrixMenu
from cpu_dash_board import CPUDashBoard

from images.CB_ico import img as icon

class WindowsManager():
    __windows_dict = {}
    __default_window = Windows.STSTEM_INFO
    def __init__(self, args) -> None:
        self.app = QtWidgets.QApplication(args)
        self.app.setWindowIcon(utils.get_icon_from_base64(icon))
        self.__register_windows()
        self.tray = TrayButton()
        self.tray.switch_floatball_signal.connect(self.switch_floatball)
        self.__current_window = self.__default_window
        self.__history_window = self.__current_window

    def __register_windows(self):
        self.__windows_dict[Windows.STSTEM_INFO] = FloatBall(self.app)
        self.__windows_dict[Windows.STSTEM_INFO].left_click_ball.connect(self.switch_activate_window)
        self.__windows_dict[Windows.CPU_INFO] = CPUDashBoard(self.app)
        self.__windows_dict[Windows.CPU_INFO].left_click_ball.connect(self.switch_activate_window)
        # self.__windows_dict[Windows.DEFAULT].right_click_ball.connect(self.switch_activate_window)
        self.__windows_dict[Windows.LEFT] = MatrixMenu(self.app)
        self.__windows_dict[Windows.LEFT].switch_default.connect(self.switch_activate_window)


    def show(self) -> int:
        '''显示主窗口'''
        screen = utils.get_focus_screen(self.app)
        self.switch_activate_window(screen.geometry().center(), self.__current_window)
        return self.app.exec()

    @QtCore.Slot(Windows)
    def switch_activate_window(self, center: QtCore.QPoint, target: Windows) -> None:
        '''切换活动窗口'''
        # print("center is {0}".format(center))
        if target is None:
            target = self.__history_window
        for win in self.__windows_dict.values():
            if not win.isHidden():
                win.hide()
        self.__windows_dict[target].set_origin(center)
        self.__windows_dict[target].activate()
        self.__history_window = self.__current_window
        self.__current_window = target

    @QtCore.Slot(Windows)
    def switch_floatball(self) -> None:
        '''切换悬浮球'''
        # print("center is {0}".format(center))
        if self.__default_window == Windows.STSTEM_INFO:
            self.__default_window = Windows.CPU_INFO
            screen = utils.get_focus_screen(self.app)
            self.switch_activate_window(screen.geometry().center(), self.__default_window)
        elif self.__default_window == Windows.CPU_INFO:
            self.__default_window = Windows.STSTEM_INFO
            screen = utils.get_focus_screen(self.app)
            self.switch_activate_window(screen.geometry().center(), self.__default_window)
        else:
            pass