from yapsy.PluginManager import PluginManager
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.IPlugin import IPlugin
import os

import logging

# Disable logging from yapsy
logger = logging.getLogger('yapsy')
logger.disabled = True

def get_plugin_dir_path():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir_path = os.path.join(curr_dir, 'plugins')
    return plugin_dir_path

class RpcPluginManager:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = RpcPluginManager()

        return cls._instance

    def __init__(self):
        self._plugin_locator = PluginFileLocator()
        plugin_dir = get_plugin_dir_path()
        plugin_places = (plugin_dir,)
        self._plugin_locator.setPluginPlaces(plugin_places)

        self._plugin_manager = PluginManager(categories_filter={"Default": IPlugin}, plugin_locator=self._plugin_locator)
        self._plugin_manager.collectPlugins()

        self._plugins_by_namespace = {}

        # Sort RPC objects taken from plugin by namespace
        for plugin_info in self._plugin_manager.getAllPlugins():
            # RPC object containing methods that are actual RPC calls
            obj = plugin_info.plugin_object

            # RPC namespace - name of the plugin module
            namespace = os.path.basename(plugin_info.path)
            self._plugins_by_namespace[namespace] = obj

    def get_rpc_object(self, namespace):
        return self._plugins_by_namespace.get(namespace, None)

    def get_namespaces_list(self):
        return self._plugins_by_namespace.keys()
