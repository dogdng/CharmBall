# -*- coding: utf-8 -*-

import sys
from windows_manager import WindowsManager
from plugin_manager import PluginManager
from plugins import *

if __name__ == "__main__":
    main = WindowsManager(sys.argv)
    try:
        processor = PluginManager()
        processed = processor.process(text="**foo bar**", plugins=('plugin1', ))
        print(processed)
        processed = processor.process(text="--foo bar--")
        print(processed)
    except Exception as ex:
        # TODO：插件崩了要给出必要的提示
        print(ex)
    finally:
        pass
    # 插件出了任何问题都不应影响核心功能的运行
    sys.exit(main.show())
