import os
from bottle import run, Bottle, redirect, static_file, view, abort
from beaker.middleware import SessionMiddleware
from hashlib import sha512

from config import HOST_ADDRESS, HOST_PORT, AUTORELOAD, SITE_NAME
from app.content import listify_posts
from app.db import FShopDBSys

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
fshop_bottle = Bottle()
fsdb = FShopDBSys(u'sdb', u'mongo', u'mongo', u'mongo', {'mongo_address': '192.168.0.189'})


#### Basic Routes ####
@fshop_bottle.get('/')
def index():
    mane = fsdb.route_db.get_mane_mane()
    redirect("/{0}".format(mane))


@fshop_bottle.route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=static_dir)


@fshop_bottle.error(404)
@view('index')
def error404(error):
    mane = fsdb.route_db.get_mane_mane()
    pm = get_page_model(mane)
    return pm


#### View Routes ####
@fshop_bottle.get('/<mane>')
@view('index')
def mane(mane):
    if not fsdb.route_db.validate_mane(mane):
        abort(404)
    pm = get_page_model(mane)
    return pm


@fshop_bottle.get('/<mane>/<tail>')
@view('index')
def tail(mane, tail):
    if not fsdb.route_db.validate_tail(mane, tail):
        abort(404)
    pm = get_page_model(mane, tail)
    return pm


#### User Routes ####
@fshop_bottle.post('/login')
def login():
    form = fshop_bottle.request.forms
    user = verify_login(form['user_id'], form['password'])
    session = fshop_bottle.request.environ.get('beaker.session')
    session['logged_in'] = True
    session['user_id'] = user

    redirect(form['selected_url'])


#### Helpers ####
def verify_login(user_id, password):
    prepared_pass = unicode(sha512(u'KsdfKSDFGT435Jwef45TJ6' + unicode(password)).hexdigest())
    user = fsdb.user_db.get_user(user_id, prepared_pass)
    if not user:
        redirect('/')

    return user


def get_page_model(mane, tail=None):
    manes, tails = fsdb.route_db.get_links_for_mane(mane)
    mane = mane.lower()
    if tail:
        tail = tail.lower()
    route = "{0}/{1}".format(mane, tail) if tail else mane
    rows = listify_posts(fsdb.content_db, route)
    return {
        'manelinks': manes,
        'taillinks': tails,
        'selected_mane': mane,
        'selected_tail': tail,
        'site_name': SITE_NAME,
        'rows': rows
    }


#### Main ####
if __name__ == "__main__":
    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': 900,
        'session.auto': True
    }
    fshop_bottle = SessionMiddleware(fshop_bottle, session_opts)
    run(fshop_bottle, host=HOST_ADDRESS, port=HOST_PORT, reloader=AUTORELOAD)
