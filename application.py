import os
from bottle import run, Bottle, redirect, static_file, view, abort

from config import HOST_ADDRESS, HOST_PORT, AUTORELOAD, SITE_NAME
from app.content import listify_posts
from app.db import FShopDBSys

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
fshop_bottle = Bottle()
fsdb = FShopDBSys(mongo_address='192.168.0.189')


#### Basic Routes ####
@fshop_bottle.get('/')
def index():
    mane = fsdb.sdb.get_mane_mane()
    redirect("/{0}".format(mane))


@fshop_bottle.route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=static_dir)


@fshop_bottle.error(404)
@view('index')
def error404(error):
    mane = fsdb.sdb.get_mane_mane()
    pm = get_page_model(mane)
    return pm


@fshop_bottle.get('/<mane>')
@view('index')
def mane(mane):
    if not fsdb.sdb.validate_mane(mane):
        abort(404)
    pm = get_page_model(mane)
    return pm


@fshop_bottle.get('/<mane>/<tail>')
@view('index')
def tail(mane, tail):
    if not fsdb.sdb.validate_tail(mane, tail):
        abort(404)
    pm = get_page_model(mane, tail)
    return pm


def get_page_model(mane, tail=None):
    manes, tails = fsdb.sdb.get_links_for_mane(mane)
    mane = mane.lower()
    if tail:
        tail = tail.lower()
    route = "{0}/{1}".format(mane, tail) if tail else mane
    rows = listify_posts(fsdb.mongo, route)
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

    run(fshop_bottle, host=HOST_ADDRESS, port=HOST_PORT, reloader=AUTORELOAD)
