import os
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from jinja2 import TemplateNotFound
from starlette.templating import Jinja2Templates
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension


class SettingsWebinterfaceExtension(WebinterfaceExtension):
    def __init__(self, parent_plugin: Plugin, templates: Jinja2Templates):
        super().__init__(parent_plugin, "settings", templates)

    def setup_router(self) -> None:
        @self.router.get("/", response_class=HTMLResponse)
        async def settings_main(request: Request):
            settings = self.parent_plugin.environment.settings.get_settings()
            return self.templates.TemplateResponse("settings/settings_page.j2", {"request": request, "settings": settings})