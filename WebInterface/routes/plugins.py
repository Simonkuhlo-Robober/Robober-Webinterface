import os
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from jinja2 import TemplateNotFound
from starlette.templating import Jinja2Templates
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension
from SimonsPluginResources.settings.models.scope import ScopePlugin


class PluginWebinterfaceExtension(WebinterfaceExtension):
    def __init__(self, parent_plugin: Plugin, templates: Jinja2Templates):
        super().__init__(parent_plugin, "plugins", templates)

    def setup_router(self) -> None:
        @self.router.get("/", response_class=HTMLResponse)
        async def plugin_interface(request: Request):
            plugins = self.parent_plugin.host_plugin.get_loaded_plugins()
            return self.templates.TemplateResponse("/plugins/plugin_list.j2", {"request": request, "plugins": plugins, "Status": Status})

        @self.router.get("/{plugin_id}", response_class=HTMLResponse)
        async def plugin_details(request: Request, plugin_id: str):
            plugin = self.parent_plugin.host_plugin.get_loaded_plugin(PluginRequest(plugin_id))
            return self.templates.TemplateResponse("plugins/plugin_inspector.j2",
                                              {"request": request, "plugin": plugin, "Status": Status})

        @self.router.get("/{plugin_id}/plugin_view", response_class=HTMLResponse)
        async def plugin_view(request: Request, plugin_id: str):
            plugin = self.parent_plugin.host_plugin.get_loaded_plugin(PluginRequest(plugin_id))
            module_path = plugin.get_module_path()
            rel_path = os.path.abspath(module_path)
            target_file_path = f"{rel_path}/External/WebInterface"
            temp_templates = Jinja2Templates(target_file_path)
            try:
                return temp_templates.TemplateResponse("view.j2", {"request": request, "plugin": plugin})
            except TemplateNotFound:
                return self.templates.TemplateResponse("plugins/view_not_found.j2", {"request": request, "plugin": plugin})

        @self.router.get("/{plugin_id}/plugin_settings", response_class=HTMLResponse)
        async def plugin_settings(request: Request, plugin_id: str):
            plugin = self.parent_plugin.host_plugin.get_loaded_plugin(PluginRequest(plugin_id))
            #settings = self.parent_plugin.environment.settings.get_settings(SettingScopeFilter(PluginScope(plugin.plugin_id)))
            return self.templates.TemplateResponse("plugins/plugin_settings.j2", {"request": request, "plugin": plugin})

        @self.router.get("/{plugin_id}/plugin_integrations", response_class=HTMLResponse)
        async def plugin_integrations(request: Request, plugin_id: str):
            plugin = self.parent_plugin.host_plugin.get_loaded_plugin(PluginRequest(plugin_id))
            return self.templates.TemplateResponse("plugins/plugin_integrations.j2", {"request": request, "plugin": plugin})

        @self.router.get("/{plugin_id}/plugin_logs", response_class=HTMLResponse)
        async def plugin_logs(request: Request, plugin_id: str):
            plugin = self.parent_plugin.host_plugin.get_loaded_plugin(PluginRequest(plugin_id))
            return self.templates.TemplateResponse("plugins/plugin_logs.j2", {"request": request, "plugin": plugin})