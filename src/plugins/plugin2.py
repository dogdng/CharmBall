# 第二个插件！
from plugin_manager import *

@PluginManager.register('plugin2')
class CleanMarkdownItalic(PluginBase):
    def __init__(self) -> None:
        super().__init__()

    def activate(self):
        return "activate plugin2"

    def clicked(self):
        return super().clicked()
