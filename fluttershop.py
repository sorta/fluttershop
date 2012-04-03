import os
from bottle import run, Bottle, redirect, static_file, view, debug

from beaker.middleware import SessionMiddleware

from config import FShopConfig
from app.db import FShopDBSys
from app.util import FShopUtil
from app.auth import FShopAuth
from app.tabs import FShopTabs

fshop_bottle = Bottle()


class FShopApp(object):

    def __init__(self):
        self._config = FShopConfig()
        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._static_dir = os.path.join(self._current_dir, 'static')

        self._FSDBsys = FShopDBSys(self._config)
        self._util = FShopUtil(self._config, self._FSDBsys, fshop_bottle)
        self._auth = FShopAuth(self._config, self._FSDBsys, fshop_bottle)
        self._tabs = FShopTabs(self._config, self._FSDBsys, fshop_bottle, self._auth, self._util)

        fshop_bottle.get('/')(self.index)
        fshop_bottle.route('/static/<filepath:path>')(self.send_static)
        fshop_bottle.route('/favicon.ico')(self.send_favicon)
        fshop_bottle.error(404)(self.error404)

    #### Basic Routes ####
    def index(self):
        mane = self._FSDBsys.route_db.get_mane_mane()
        redirect("/{0}".format(mane))

    def send_static(self, filepath):
        return static_file(filepath, root=self._static_dir)

    def send_favicon(self):
        return static_file('fluttershop16.ico', root=self._static_dir)

    @view('main')
    def error404(self, error):
        mane = self._FSDBsys.route_db.get_mane_mane()
        pm = self.get_page_model(mane)
        return pm

    def start(self):
        session_opts = {
            'session.type': 'memory',
            'session.cookie_expires': 900,
            'session.auto': True
        }
        if self._config.debug:
            debug(True)
        wrapped_bottle = SessionMiddleware(fshop_bottle, session_opts)

        run(wrapped_bottle, host=self._config.host_address, port=self._config.host_port, reloader=self._config.autoreload)


#### Main ####
if __name__ == "__main__":

    fsapp = FShopApp()
    fsapp.start()