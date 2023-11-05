from enum import Enum, unique, auto

@unique
class Windows(Enum):
    '''窗口枚举'''
    STSTEM_INFO = auto()
    CPU_INFO = auto()
    LEFT = auto()
    RIGHT = auto()
    # TRAY = auto() 系统托盘图标不属于窗口

    def __str__(self):
        return 'Current window is {0}'.format(self.name)
