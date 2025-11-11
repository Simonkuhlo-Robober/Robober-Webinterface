from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin import Plugin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SimonsPluginResources.plugin_host import HostPlugin
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.settings.scopes import PluginScope
from SimonsPluginResources.settings.setting import Setting
from .main import WebInterfacePluginExtension

class WebInterfacePlugin(Plugin):
    def __init__(self, environment: Environment):
        super().__init__(plugin_id = "WEBINTERFACE",
                         environment = environment,
                         name = "Webinterface",
                         description = "Webinterface",
                         version = 1,
                         used_host_version = 0,
                         plugin_connections=[PluginRequest("HOST", 0, True)]
                         )
        self.host_plugin: "HostPlugin" = None
        self.add_plugin_extension(WebInterfacePluginExtension(self))

    def get_settings(self) -> list[Setting]:
        return [
            Setting("webinterface",
                    "host_address",
                    "Networking",
                    scope=PluginScope(self.plugin_id),
                    default_value="localhost",
                    )
        ]

    def add_plugin_link(self, plugin:"Plugin") -> None:
        super().add_plugin_link(plugin)
        if plugin.plugin_id == "HOST":
            self.host_plugin = plugin

def get_plugin(environment: Environment):
    return WebInterfacePlugin(environment)