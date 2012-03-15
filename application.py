import cherrypy
import os

from views import index
from fshopconf import FSSettings


class FSContext:

    def __init__(self, appdir):
        self._app_dir = appdir

    @property
    def app_dir(self):
        return self._app_dir


def build_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    settings = FSSettings(current_dir)

    # Use the configuration file tutorial.conf.
    cherrypy.config.update(settings.global_settings)
    cherrypy.quickstart(index.MainApp(), "/", settings.standard_settings)

if __name__ == '__main__':

    build_app()
