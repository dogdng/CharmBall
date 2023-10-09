from plugin_manager import *

@PluginManager.register('ReturnBall')
class ReturnBall(PluginBase):
    def __init__(self) -> None:
        super().__init__()

    def activate(self):
        return "activate plugin: return_ball"

    def clicked(self):
        return super().clicked()
