import os
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from jinja2 import TemplateNotFound
from starlette.templating import Jinja2Templates
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.settings import Setting
from SimonsPluginResources.settings.filters.scope_filter import SettingFilterScope
from SimonsPluginResources.settings.models.scope import ScopePlugin
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension


class SettingsWebinterfaceExtension(WebinterfaceExtension):
    def __init__(self, parent_plugin: Plugin, templates: Jinja2Templates):
        super().__init__(parent_plugin, "settings", templates)

    def setup_router(self) -> None:
        @self.router.get("/", response_class=HTMLResponse)
        async def settings_main(request: Request, plugin: str = None, clean:bool = False):
            returned_settings = self.parent_plugin.environment.settings.get_list()
            if plugin:
                returned_settings = SettingFilterScope(ScopePlugin(plugin_id=plugin)).filter_ist(returned_settings)
            if clean:
                return self.templates.TemplateResponse("settings/settings_editor.j2", {"request": request, "settings": returned_settings})
            return self.templates.TemplateResponse("settings/settings_page.j2", {"request": request, "settings": returned_settings})