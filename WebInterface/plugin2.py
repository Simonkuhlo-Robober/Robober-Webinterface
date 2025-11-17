from typing import Optional, TYPE_CHECKING
from SimonsPluginResources.asyncio_task_wrapper import AsyncTask
from SimonsPluginResources.plugin import Plugin, PluginMeta
from SimonsPluginResources.settings import Setting
from SimonsPluginResources.settings.models.scope import ScopePlugin
from . import main
if TYPE_CHECKING:
    from SimonsPluginResources.plugin_host import PluginHost

class WebInterfacePluginMeta(PluginMeta):
    def __init__(self):
        super().__init__(plugin_id = "webinterface")
        self.name = "Webinterface"
        self.description = "No description provided"
        self.version = 2
        self.used_backend_version = 10
        self.connection_requests = None
        self.settings = [
            Setting(rel_path="host_address", default_value="localhost", scope=ScopePlugin(plugin_id=self.plugin_id),
                    comment="Webinterface must be restarted after changing value!"),
            Setting(rel_path="port", default_value="8080", scope=ScopePlugin(plugin_id=self.plugin_id),
                    comment="Webinterface must be restarted after changing value!")
        ]

class WebInterfacePlugin(Plugin):
    def __init__(self, host: "PluginHost"):
        super().__init__(host, WebInterfacePluginMeta())
        self.webinterface = main.WebInterface(self)

    @property
    def tasks(self) -> Optional[list[AsyncTask]]:
        return[AsyncTask(self.webinterface.run_webinterface(), "Webinterface main loop")]
