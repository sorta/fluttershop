import os
from bottle import run, Bottle, redirect, static_file, view, abort, debug

from beaker.middleware import SessionMiddleware
from hashlib import sha512

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
        form = fshop_bottle.request.forms
        user = self.verify_login(form['user_id'], form['password'])
        session = fshop_bottle.request.environ.get('beaker.session')
        session['logged_in'] = True
        session['user_id'] = user

        redirect(form['selected_url'])

    #### Helpers ####
    def verify_login(self, user_id, password):
        prepared_pass = unicode(sha512(u'KsdfKSDFGT435Jwef45TJ6' + unicode(password)).hexdigest())
        user = self._FSDBsys.user_db.get_user(user_id, prepared_pass)
        if not user:
            redirect('/')

        return user

    def get_page_model(self, mane, tail=None):
        manes, tails = self._FSDBsys.route_db.get_links_for_mane(mane)
        mane = mane.lower()
        if tail:
            tail = tail.lower()
        route = "{0}/{1}".format(mane, tail) if tail else mane
        rows = listify_posts(self._FSDBsys.content_db, route)
        return {
            'manelinks': manes,
            'taillinks': tails,
            'selected_mane': mane,
            'selected_tail': tail,
            'site_name': self._config.site_name,
            'rows': rows
        }

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
