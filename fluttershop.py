import os
from bottle import run, Bottle, redirect, static_file, view, debug, response

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
        fshop_bottle.get('/')(self.index)
        fshop_bottle.route('/static/<filepath:path>')(self.send_static)
        fshop_bottle.route('/favicon.ico')(self.send_favicon)
        fshop_bottle.error(404)(self.error404)

        self._config = FShopConfig()
        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._static_dir = os.path.join(self._current_dir, 'static')

        self._base_util = FShopBaseUtil()
        self._crypto = FShopCrypto()
        self._FSDBsys = FShopDBSys(self._base_util, self._config, self._crypto)
        self._util = FShopUtil(self._base_util, self._config, self._FSDBsys, fshop_bottle)
        self._auth = FShopAuth(self._base_util, self._config, self._FSDBsys, fshop_bottle)
        self._content = FShopContent(self._base_util, self._config, self._FSDBsys, fshop_bottle, self._auth, self._util)
        self._site_options = FShopSiteOptions(self._base_util, self._util, self._FSDBsys, self._auth, self._crypto, fshop_bottle)

        # For routing reasons, tabs should be the last module to load
        self._tabs = FShopTabs(self._base_util, self._config, self._FSDBsys, fshop_bottle, self._auth, self._util)

    #### Basic Routes ####
    def index(self):
        mane = self._FSDBsys.route_db.get_mane_tab()
        if mane:
            redirect(mane.get('path', '/home'))
        else:
            rank = self._FSDBsys.route_db.get_next_tab_rank(None)
            def_ppp = self._FSDBsys.options_db.get_def_ppp_num()
            self._FSDBsys.route_db.add_new_tab("Home", rank, "Site Home", "FlutterShop default home", parent_id=None, nav_display=True, ppp=def_ppp)
            redirect("/home")

    def send_static(self, filepath):
        return static_file(filepath, root=self._static_dir)

    def send_favicon(self):
        return static_file('favicon.ico', root=self._static_dir)

    @view('main')
    def error404(self, error):
        tab = self._FSDBsys.route_db.get_tab_by_name('/404')
        pm = self._util.get_page_model(tab)
        return pm

    def init_db_if_necessary(self):
        site_name = self._FSDBsys.options_db.get_site_name()
        if not site_name:
            self._FSDBsys.options_db._add_site_name("FlutterShop")

        def_ppp = self._FSDBsys.options_db.get_def_ppp()
        if not def_ppp:
            self._FSDBsys.options_db._add_def_ppp(10)

        if not self._FSDBsys.options_db.at_least_one_user():
            self._FSDBsys.options_db._add_user("admin", "123456", "example@email.com")

        error_tab = self._FSDBsys.route_db.get_tab_by_name('404')
        if not error_tab:
            def_ppp = self._FSDBsys.options_db.get_def_ppp_num()
            error_tab = self._FSDBsys.route_db.add_new_tab('404', 0, title='Page Not Found', desc='The page you are looking for does not exist.', parent_id=None, nav_display=False, ppp=def_ppp)
        else:
            error_tab = error_tab['_id']

        error_posts = self._FSDBsys.content_db.get_posts_for_tab(error_tab, post_limit=10)
        if not error_posts.count():
            self._FSDBsys.content_db.insert_new_post(error_tab, "left", 12, "Page Not Found", 0, True, False, "<p>You've tried to access a non-existant page.</p>")

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
