# -*- coding: utf-8 -*-

import os, PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TrayButton(QWidget):
    '''
    系统托盘按钮
    '''
    def __init__(self) -> None:
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        # 系统托盘
        self.config_tray()

    def config_tray(self):
        self.tray_icon.setIcon(QIcon("./resources/EasingFunctionsIcon.png"))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        # self.tray_icon.show()

        # 创建右键菜单
        self.tray_menu = QMenu(self)
        self.close_action = QAction("退出", self)
        self.close_action.triggered.connect(QCoreApplication.quit)
        self.tray_menu.addAction(self.close_action)

        # 将右键菜单添加到系统托盘图标
        self.tray_icon.setContextMenu(self.tray_menu)

        # 显示系统托盘图标
        self.tray_icon.show()


    """
    系统托盘
    """
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            print("tray button triggered!")

