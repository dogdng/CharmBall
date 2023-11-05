# -*- coding: utf-8 -*-

import os, PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import utils
from images.CB_ico import img as icon

class TrayButton(QWidget):
    '''系统托盘按钮'''
    switch_floatball_signal = QtCore.Signal() # 信号必须放在方法外面
    def __init__(self) -> None:
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        # 系统托盘
        self.tray_icon.setIcon(utils.get_icon_from_base64(icon))
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 创建右键菜单
        self.tray_menu = QMenu(self)
        self.switch_floatball_action = QAction("切换视图", self)
        self.switch_floatball_action.triggered.connect(self.switch_floatball)
        self.close_action = QAction("退出", self)
        self.close_action.triggered.connect(QtCore.QCoreApplication.quit)
        self.tray_menu.addAction(self.switch_floatball_action)
        self.tray_menu.addAction(self.close_action)

        # 将右键菜单添加到系统托盘图标
        self.tray_icon.setContextMenu(self.tray_menu)

        # 显示系统托盘图标
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """单击系统托盘槽函数"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print("tray button triggered!")

    def switch_floatball(self):
        """切换悬浮球槽函数"""
        self.switch_floatball_signal.emit()

