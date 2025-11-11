import os
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from jinja2 import TemplateNotFound
from starlette.templating import Jinja2Templates
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.settings.setting_filter import SettingFilterCollection, SettingCategoryFilter, SettingScopeFilter
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension
from SimonsPluginResources.settings.scopes import PluginScope
from typing import Optional


class APIWebinterfaceExtension(WebinterfaceExtension):
    def __init__(self, parent_plugin: Plugin, templates: Jinja2Templates):
        super().__init__(parent_plugin, "api", templates)

    def setup_router(self) -> None:
        @self.router.get("/filtered_list/", response_class=HTMLResponse)
        async def settings_api(request: Request, plugin_id: Optional[str] = None, category: Optional[str] = None):
            filter_collection = SettingFilterCollection()
            if plugin_id:
                filter_collection.add_filter(SettingScopeFilter(PluginScope(plugin_id)))
            if category:
                filter_collection.add_filter(SettingCategoryFilter(category))
            settings = self.parent_plugin.environment.settings.get_settings(filter_collection)
            setting_names: list[str] = []
            for setting in settings:
                setting_names.append(f"{setting.topic}.{setting.setting_id}")
            return JSONResponse({"settings": setting_names})
