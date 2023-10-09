# -*- coding: utf-8 -*-

import os, PySide6
from time import sleep

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PySide6 import QtGui, QtWidgets, QtCore

from interface import Windows
import utils
from tray_button import TrayButton
from float_ball import FloatBall
from left_click_window import LeftClickWindow

# from plugin_manager import PluginManager
# from plugins import *


class WindowsManager():
    __windows_dict = {}
    __current_window = Windows.BALL

    def __init__(self, args) -> None:
        self.app = QtWidgets.QApplication(args)
        self.__register_windows()
        self.tray = TrayButton()

        # try:
        #     plugin = PluginManager()
        #     processed = plugin.load()
        # except Exception as ex:
        #     # TODO：插件出错要给出必要的提示
        #     print(ex)
        # finally:
        #     pass

    def __register_windows(self):
        self.__windows_dict[Windows.BALL] = FloatBall(self.app)
        self.__windows_dict[Windows.BALL].click_ball.connect(self.switch_activate_window)
        self.__windows_dict[Windows.LEFT] = LeftClickWindow(self.app)
        self.__windows_dict[Windows.LEFT].switch_ball.connect(self.switch_activate_window)

    def show(self) -> int:
        screen = utils.get_focus_screen(self.app)
        self.switch_activate_window(self.__current_window, screen.geometry().center())
        return self.app.exec()

    @QtCore.Slot(Windows)
    def switch_activate_window(self, target: Windows, center: QtCore.QPoint) -> None:
        # print("center is {0}".format(center))
        for win in self.__windows_dict.values():
            if not win.isHidden():
                win.hide()
        self.__windows_dict[target].set_origin(center)
        self.__windows_dict[target].activate()