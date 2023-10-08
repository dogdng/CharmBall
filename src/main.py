# -*- coding: utf-8 -*-

import sys
from windows_manager import WindowsManager

if __name__ == "__main__":
    main = WindowsManager(sys.argv)
    sys.exit(main.show())
