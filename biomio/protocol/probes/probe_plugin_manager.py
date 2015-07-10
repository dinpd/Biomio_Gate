import os
from threading import Lock
from yapsy.IPlugin import IPlugin
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginManager import PluginManager


class ProbePluginManager:
    _instance = None
    _lock = Lock()
    _PLUGIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = ProbePluginManager()
        return cls._instance

    def __init__(self):
        self._plugin_locator = PluginFileLocator()
        self._plugin_locator.setPluginPlaces((self._PLUGIN_DIR, ))

        self._plugin_manager = PluginManager(categories_filter={'Default': IPlugin},
                                             plugin_locator=self._plugin_locator)
        self._plugin_manager.collectPlugins()

        self._plugins_by_probe_type = {}

        for plugin_info in self._plugin_manager.getAllPlugins():
            self._plugins_by_probe_type.update({os.path.basename(plugin_info.path): plugin_info.plugin_object})

    def get_plugin_object(self, probe_type):
        return self._plugins_by_probe_type.get('%s_plugin' % probe_type, None)
