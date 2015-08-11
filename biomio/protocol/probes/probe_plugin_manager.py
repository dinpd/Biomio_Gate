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
        self._plugin_locator.setPluginPlaces((self._PLUGIN_DIR,))

        self._plugin_manager = PluginManager(categories_filter={'Default': IPlugin},
                                             plugin_locator=self._plugin_locator)
        self._plugin_manager.collectPlugins()
        self._enabled_plugin_types = []

        for plugin_info in self._plugin_manager.getAllPlugins():
            if self.is_plugin_enabled(plugin_info.name):
                self._plugin_manager.activatePluginByName(name=plugin_info.name)
                self._enabled_plugin_types.append(plugin_info.name)
            else:
                self._plugin_manager.deactivatePluginByName(name=plugin_info.name)

    def _get_plugin_info_by_name(self, plugin_name):
        plugin_info = self._plugin_manager.getPluginByName(name=plugin_name)
        if plugin_info is None:
            raise KeyError("No plugin found for given name - %s" % plugin_name)
        return plugin_info

    def is_plugin_enabled(self, probe_type):
        plugin_info = self._get_plugin_info_by_name(probe_type)
        return plugin_info.details.has_option("Documentation", "Enabled") and bool(
            plugin_info.details.get("Documentation", "Enabled"))

    def get_plugin_by_name(self, probe_type):
        plugin_info = self._get_plugin_info_by_name(probe_type)
        return plugin_info.plugin_object

    def get_enabled_plugin_types(self):
        return self._enabled_plugin_types
