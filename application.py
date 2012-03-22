import os
from bottle import run, Bottle, redirect, static_file, view, abort, debug, request

from beaker.middleware import SessionMiddleware

from config import FShopConfig
from app.content import listify_posts
from app.db import FShopDBSys

fshop_bottle = Bottle()


class FShopApp(object):

    def __init__(self):
        self._config = FShopConfig()
        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._static_dir = os.path.join(self._current_dir, 'static')

        self._FSDBsys = FShopDBSys(self._config)

        fshop_bottle.get('/')(self.index)
        fshop_bottle.route('/static/<filepath:path>')(self.send_static)
        fshop_bottle.route('/favicon.ico')(self.send_favicon)
        fshop_bottle.error(404)(self.error404)
        fshop_bottle.get('/<mane>')(self.mane)
        fshop_bottle.get('/<mane>/<tail>')(self.tail)
        fshop_bottle.post('/login')(self.login)
        fshop_bottle.post('/logout')(self.logout)

    #### Basic Routes ####
    def index(self):
        mane = self._FSDBsys.route_db.get_mane_mane()
        redirect("/{0}".format(mane))

    def send_static(self, filepath):
        return static_file(filepath, root=self._static_dir)

    def send_favicon(self):
        return static_file('fluttershop16.ico', root=self._static_dir)

    @view('index')
    def error404(self, error):
        mane = self._FSDBsys.route_db.get_mane_mane()
        pm = self.get_page_model(mane)
        return pm

    #### View Routes ####
    @view('index')
    def mane(self, mane):
        if not self._FSDBsys.route_db.validate_mane(mane):
            abort(404)
        pm = self.get_page_model(mane)
        return pm

    @view('index')
    def tail(self, mane, tail):
        if not self._FSDBsys.route_db.validate_tail(mane, tail):
            abort(404)
        pm = self.get_page_model(mane, tail)
        return pm

    #### User Routes ####
    def login(self):

        form = request.forms
        selected_url = form['selected_url']
        user = self.verify_login(form['login_username'], form['login_pass'], selected_url)
        session = request.environ.get('beaker.session')
        session['logged_in'] = True
        session['user'] = user

        redirect(selected_url)

    def logout(self):

        form = request.forms
        selected_url = form['selected_url']
        session = request.environ.get('beaker.session')
        session['logged_in'] = False
        session['user'] = None

        redirect(selected_url)

    #### Helpers ####
    def verify_login(self, user_id, password, selected_url):
        user = self._FSDBsys.options_db.get_user(user_id, password)
        if not user:
            redirect(selected_url)

        return user

    def get_page_model(self, mane, tail=None):
        manes, tails = self._FSDBsys.route_db.get_links_for_mane(mane)
        mane = mane.lower()
        if tail:
            tail = tail.lower()
        route = "{0}/{1}".format(mane, tail) if tail else mane
        rows = listify_posts(self._FSDBsys.content_db, route)
        return self.add_user_info({
            'manelinks': manes,
            'taillinks': tails,
            'selected_mane': mane,
            'selected_tail': tail,
            'site_name': self._config.site_name,
            'rows': rows
        })

    def add_user_info(self, pm):
        session = request.environ.get('beaker.session')
        pm['logged_in'] = session.get('logged_in', False)
        if pm['logged_in']:
            pm['user'] = session.get('user', None)
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
