from plugin_manager import *

@PluginManager.register('plugin1')
class CleanMarkdownBolds(PluginBase):
    def __init__(self) -> None:
        super().__init__()

    def process(self, text):
        return text.replace('**', '')

    def process2(self):
        return super().process2()