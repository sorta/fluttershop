import os
from bottle import run, Bottle, redirect, static_file, view, debug

from beaker.middleware import SessionMiddleware

from config import FShopConfig
from app.db import FShopDBSys
from app.util import FShopUtil, FShopBaseUtil
from app.auth import FShopAuth
from app.tabs import FShopTabs
from app.content import FShopContent
from app.crypto import FShopCrypto
from app.site_options import FShopSiteOptions

fshop_bottle = Bottle()


class FShopApp(object):

    def __init__(self):
        self._config = FShopConfig()
        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._static_dir = os.path.join(self._current_dir, 'static')

        self._base_util = FShopBaseUtil()
        self._crypto = FShopCrypto()
        self._FSDBsys = FShopDBSys(self._base_util, self._config, self._crypto)
        self._util = FShopUtil(self._base_util, self._config, self._FSDBsys, fshop_bottle)
        self._auth = FShopAuth(self._base_util, self._config, self._FSDBsys, fshop_bottle)
        self._tabs = FShopTabs(self._base_util, self._config, self._FSDBsys, fshop_bottle, self._auth, self._util)
        self._content = FShopContent(self._base_util, self._config, self._FSDBsys, fshop_bottle, self._auth, self._util)
        self._content = FShopSiteOptions(self._base_util, self._FSDBsys, self._auth, self._crypto, fshop_bottle)

        fshop_bottle.get('/')(self.index)
        fshop_bottle.route('/static/<filepath:path>')(self.send_static)
        fshop_bottle.route('/favicon.ico')(self.send_favicon)
        fshop_bottle.error(404)(self.error404)

    #### Basic Routes ####
    def index(self):
        mane = self._FSDBsys.route_db.get_mane_mane()
        if mane:
            redirect(mane.get('route_name', '/Home'))
        else:
            priority = self._FSDBsys.rank_db.get_next_mane_rank()
            self._FSDBsys.route_db.add_new_mane("Home", priority, "Site Home", "FlutterShop default home")
            self._FSDBsys.rank_db.increment_mane_rank()
            redirect("/home")

    def send_static(self, filepath):
        return static_file(filepath, root=self._static_dir)

    def send_favicon(self):
        return static_file('fluttershop16.ico', root=self._static_dir)

    @view('main')
    def error404(self, error):
        mane = self._FSDBsys.route_db.get_mane_mane().get('mane_name', '/')
        pm = self._util.get_page_model(mane)
        return pm

    def init_db_if_necessary(self):
        site_name = self._FSDBsys.options_db.get_site_name()
        if not site_name:
            self._FSDBsys.options_db._add_site_name("FlutterShop")

        if not self._FSDBsys.options_db.at_least_one_user():
            self._FSDBsys.options_db._add_user("admin", "12345", "example@email.com")

    def start(self):
        self.init_db_if_necessary()

        session_opts = {
            'session.type': 'memory',
            'session.timeout': 900,
            'session.auto': True
        }
        wrapped_bottle = SessionMiddleware(fshop_bottle, session_opts)

        if self._config.debug:
            debug(True)

        run(wrapped_bottle, host=self._config.host_address, port=self._config.host_port, reloader=self._config.autoreload, server=self._config.server)


#### Main ####
if __name__ == "__main__":

    fsapp = FShopApp()
    fsapp.start()
