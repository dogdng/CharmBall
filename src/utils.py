# -*- coding: utf-8 -*-

import os, PySide6
import sys, threading, time
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


# 渐变透明度
def anime_WindowOpacity(window):
    window.setWindowOpacity(0)
    n = 0.0
    for i in range(15):
        time.sleep(0.01)
        n += 0.06
        window.setWindowOpacity(n)


# devicePixelRatio不能正确获得缩放系数，因此重新计算缩放系数
def get_devicePixelRatio(screen):
    logicalDpi = screen.logicalDotsPerInch()
    physicalDpi = screen.physicalDotsPerInch()

    # 计算缩放比例
    devicePixelRatio = logicalDpi / physicalDpi
    return devicePixelRatio


# 获得焦点屏幕
def get_focus_screen(app):
    # 根据四周有无屏幕，哪些方向的拖动时允许的
    screens = app.screens()
    # 首先判断焦点屏幕
    # 判断激活的屏幕的序号
    for index, screen in enumerate(screens):
        screen_geometry = screen.geometry()
        x, y, width, height = (
            screen_geometry.x(),
            screen_geometry.y(),
            screen_geometry.width(),
            screen_geometry.height(),
        )
        scale_factor = get_devicePixelRatio(screen)
        # scale_factor = screen.devicePixelRatio()
        cursor_pos = QCursor.pos()
        # 判断鼠标在不在该屏幕内
        if x <= cursor_pos.x() < x + width * scale_factor and y <= cursor_pos.y() < y + height * scale_factor:
            break

    # print("激活屏幕为：",index)

    # 将焦点屏幕从screens列表取出
    focus_screen = screens.pop(index)

    return focus_screen
