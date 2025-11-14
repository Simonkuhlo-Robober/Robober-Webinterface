from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.requests import Request
from threading import Thread
from fastapi.staticfiles import StaticFiles
from SimonsPluginResources.plugin_extension import PluginExtension
from SimonsPluginResources.webinterface_extension import WebinterfaceExtension
from starlette.templating import Jinja2Templates
from .routes.plugins import PluginWebinterfaceExtension
from .routes.settings import SettingsWebinterfaceExtension
from .routes.api import APIWebinterfaceExtension
import uvicorn
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import WebInterfacePlugin


class WebInterfacePluginExtension(PluginExtension):
    def __init__(self, parent_plugin: "WebInterfacePlugin" = None):
        super().__init__(parent_plugin)
        # Get the directory where the current file is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir_path = os.path.join(base_dir, "static")

        self.app = FastAPI()
        self.app.mount("/static", StaticFiles(directory=static_dir_path), name="static")
        self.templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
        self.add_extension(PluginWebinterfaceExtension(self.parent_plugin, self.templates))
        self.add_extension(SettingsWebinterfaceExtension(self.parent_plugin, self.templates))
        self.add_extension(APIWebinterfaceExtension(self.parent_plugin))


        @self.app.get("/")
        async def read_root():
            return RedirectResponse(url="/home", status_code=308)

        @self.app.get("/home", response_class=HTMLResponse)
        async def settings_interface(request: Request):
            return self.templates.TemplateResponse("home_page.j2", {"request": request})

        @self.app.get("/status", response_class=HTMLResponse)
        async def settings_interface(request: Request):
            latency = self.parent_plugin.environment.bot.latency
            return self.templates.TemplateResponse("status_page.j2", {"request": request, "latency": latency})


    def add_extension(self, extension:WebinterfaceExtension) -> None:
        self.app.include_router(extension.router)

    def run_webinterface(self):
        fallback_host: str = "localhost"
        fallback_port: int = 8000
        host = self.parent_plugin.environment.settings.get_value("Plugin.WEBINTERFACE.host_address")
        if not host:
            host = fallback_host
            self.parent_plugin.log_factory.log(f"Setting host_address not found. Using fallback ({fallback_host})")
        port = self.parent_plugin.environment.settings.get_value("Plugin.WEBINTERFACE.port")
        try:
            port = int(port)
        except ValueError:
            port = fallback_port
            self.parent_plugin.log_factory.log(f"Unable to convert port setting value to int. Using fallback ({fallback_port})")
        if not port:
            port = fallback_port
            self.parent_plugin.log_factory.log(f"Setting port not found. Using fallback ({fallback_port})")
        uvicorn.run(self.app, host=host, port=port)

    def _start(self) -> None:
        api_thread = Thread(target=self.run_webinterface, daemon=True)
        api_thread.start()

