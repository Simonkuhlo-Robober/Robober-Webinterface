from fastapi.responses import JSONResponse
from fastapi.requests import Request
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.settings import Setting
from SimonsPluginResources.settings.filters import SettingFilterCollection
from SimonsPluginResources.settings.models.setting_update import SettingUpdate
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension
from SimonsPluginResources.settings.models.scope import ScopePlugin
from typing import Optional


class APIWebinterfaceExtension(WebinterfaceExtension):
    def __init__(self, parent_plugin: Plugin):
        super().__init__(parent_plugin, "api")

    def setup_router(self) -> None:
        @self.router.get("/setting/{setting_path}")
        async def get_setting(request: Request, setting_path: str):
            return self.parent_plugin.environment.settings.get_setting(setting_path)

        @self.router.put("/setting/{setting_path}")
        async def update_setting(request: Request, setting_path: str, update: SettingUpdate):
            self.parent_plugin.environment.settings.set_current_value(setting_path, update.current_value)
            return self.parent_plugin.environment.settings.get_setting(setting_path)

        @self.router.post("/setting/{setting_path}")
        async def create_setting(request: Request, setting_path: str):
            raise NotImplementedError

        @self.router.delete("/setting/{setting_path}")
        async def delete_setting(request: Request, setting_path: str, update: SettingUpdate):
            raise NotImplementedError
