# 第二个插件！
from plugin_manager import *

@PluginManager.register('plugin2')
class CleanMarkdownItalic(PluginBase):
    def __init__(self) -> None:
        super().__init__()

    def process(self, text):
        return text.replace('--', '')

    # def process2(self):
    #     return super().process2()
