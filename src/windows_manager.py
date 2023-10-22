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

class WindowsManager():
    __windows_dict = {}
    __current_window = Windows.DEFAULT

    def __init__(self, args) -> None:
        self.app = QtWidgets.QApplication(args)
        self.__register_windows()
        self.tray = TrayButton()

    def __register_windows(self):
        self.__windows_dict[Windows.DEFAULT] = FloatBall(self.app)
        self.__windows_dict[Windows.DEFAULT].left_click_ball.connect(self.switch_activate_window)
        # self.__windows_dict[Windows.DEFAULT].right_click_ball.connect(self.switch_activate_window)
        self.__windows_dict[Windows.LEFT] = MatrixMenu(self.app)
        self.__windows_dict[Windows.LEFT].switch_default.connect(self.switch_activate_window)

    def show(self) -> int:
        '''显示主窗口'''
        screen = utils.get_focus_screen(self.app)
        self.switch_activate_window(self.__current_window, screen.geometry().center())
        return self.app.exec()

    @QtCore.Slot(Windows)
    def switch_activate_window(self, target: Windows, center: QtCore.QPoint) -> None:
        '''切换活动窗口'''
        # print("center is {0}".format(center))
        for win in self.__windows_dict.values():
            if not win.isHidden():
                win.hide()
        self.__windows_dict[target].set_origin(center)
        self.__windows_dict[target].activate()