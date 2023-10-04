import sys
from abc import ABCMeta, abstractmethod

class PluginBase(metaclass = ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, text):
        tb = sys.exception().__traceback__
        raise NotImplementedError(self.__class__.__name__).with_traceback(tb)

    @abstractmethod
    def process2(self):
        tb = sys.exception().__traceback__
        raise NotImplementedError(self.__class__.__name__).with_traceback(tb)

class PluginManager(object):
    __plugins = {}

    def process(self, text, plugins=()):
        try:
            if plugins == ():
                for plugin_name in self.__plugins.keys():
                    text = self.__plugins[plugin_name]().process(text)
            else:
                for plugin_name in plugins:
                    text = self.__plugins[plugin_name]().process(text)
            return text
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

