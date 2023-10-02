# -*- coding: utf-8 -*-

import os, sys, PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PySide6.QtWidgets import *

from float_ball import FloatBall

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = FloatBall(app)
    main.show()
    sys.exit(app.exec())
