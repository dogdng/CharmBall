import sys
from abc import ABCMeta, abstractmethod

class PluginBase(metaclass = ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def activate(self, text):
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def clicked(self):
        raise NotImplementedError(self.__class__.__name__)

class PluginManager(object):
    __plugins = {}

    def load(self):
        try:
            for plugin_name in self.__plugins.keys():
                text = self.__plugins[plugin_name]().activate()
                print(text)
        except Exception as ex:
            print("Plugin process error!")
            raise ex
        else:
            pass
        finally:
            pass

    @classmethod
    def register(cls, plugin_name):
        def wrapper(plugin):
            cls.__plugins.update({plugin_name:plugin})
            return plugin
        return wrapper

