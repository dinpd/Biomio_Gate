import ast
import logging
import os
from threading import Lock
from yapsy.IPlugin import IPlugin
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginManager import PluginManager

logger = logging.getLogger('yapsy')
logger.disabled = True

logger = logging.getLogger(__name__)


class ProbePluginManager:
    _instance = None
    _lock = Lock()
    _PLUGIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')

    _PLUGIN_OBJECT_ATTR = 'plugin_object'

    AUTH_TYPE_ATTR = 'auth_type'
    AUTH_CONFIG_ATTR = 'auth_config'
    ENABLED_ATTR = 'enabled'
    ALGO_ID_ATTR = 'algo_id'
    MAX_TRAINING_ATTR = 'max_training_attempts'
    MAX_VERIFICATION_ATTR = 'max_verification_attempts'

    _AVAILABLE_EXTRA_CONFIG_ATTR = [AUTH_TYPE_ATTR, AUTH_CONFIG_ATTR, ENABLED_ATTR, ALGO_ID_ATTR, MAX_TRAINING_ATTR,
                                    MAX_VERIFICATION_ATTR]

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

        self._plugins_data_by_auth_type = {}

        for plugin_info in self._plugin_manager.getAllPlugins():
            plugin_extra_config = self._parse_plugin_extra_config(plugin_info)
            if plugin_extra_config.get(self.ENABLED_ATTR, False):
                self._plugin_manager.activatePluginByName(name=plugin_info.name)
                plugin_extra_config.update({self._PLUGIN_OBJECT_ATTR: plugin_info.plugin_object})
                self._plugins_data_by_auth_type.update(
                    {plugin_extra_config.get(self.AUTH_TYPE_ATTR, plugin_info.name): plugin_extra_config})
            else:
                self._plugin_manager.deactivatePluginByName(name=plugin_info.name)

    def get_plugin_auth_config(self, auth_type):
        plugin_data = self._plugins_data_by_auth_type.get(auth_type)
        if plugin_data is None:
            raise KeyError('No plugin found for given auth type - %s' % auth_type)
        return plugin_data.get(self.AUTH_CONFIG_ATTR, {})

    def get_plugin_by_auth_type(self, auth_type):
        plugin_data = self._plugins_data_by_auth_type.get(auth_type)
        if plugin_data is None:
            raise KeyError('No plugin found for given auth type - %s' % auth_type)
        plugin_object = plugin_data.get(self._PLUGIN_OBJECT_ATTR)
        if plugin_object is None:
            raise KeyError('No plugin object instance found for given auth type - %s' % auth_type)
        return plugin_object

    def _parse_plugin_extra_config(self, plugin_info):
        plugin_extra_config = {}
        for extra_config_attr in self._AVAILABLE_EXTRA_CONFIG_ATTR:
            if plugin_info.details.has_option("Documentation", extra_config_attr):
                extra_config = str(plugin_info.details.get("Documentation", extra_config_attr))
                try:
                    extra_config = ast.literal_eval(extra_config)
                except ValueError as e:
                    logger.warning(e)
                    logger.debug(extra_config)
                plugin_extra_config.update({extra_config_attr: extra_config})
        plugin_info.plugin_object.set_plugin_config(plugin_extra_config)
        logger.debug('EXTRA PLUGIN CONFIG: %s ==== %s' % (plugin_info.name, plugin_extra_config))
        return plugin_extra_config

    def get_available_auth_types(self):
        return self._plugins_data_by_auth_type.keys()
