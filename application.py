import os
from bottle import run, Bottle, redirect, static_file, view, abort

from config import HOST_ADDRESS, HOST_PORT, AUTORELOAD, SITE_NAME
from app.db import FShopDB

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
fshop_bottle = Bottle()
db = FShopDB()


#### Basic Routes ####
@fshop_bottle.get('/')
def index():
    redirect("/home")


@fshop_bottle.route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=static_dir)


@fshop_bottle.error(404)
def error404(error):
    return 'Nothing here, sorry'


@fshop_bottle.get('/<mane>')
@view('index')
def mane(mane):
    if not db.validate_mane(mane):
        abort(404)
    pm = get_page_model(mane)
    pm['data'] = 'Hello World!'
    return pm


@fshop_bottle.get('/<mane>/<tail>')
@view('index')
def tail(mane, tail):
    if not db.validate_tail(mane, tail):
        abort(404)
    pm = get_page_model(mane, tail)
    pm['data'] = 'Hello World!'
    print pm
    return pm


def get_page_model(mane, tail=None):
    manes, tails = db.get_links_for_mane(mane)
    return {
        'manelinks': manes,
        'taillinks': tails,
        'selected_mane': mane.lower() if mane else mane,
        'selected_tail': tail.lower() if tail else tail,
        'site_name': SITE_NAME
    }


#### Main ####
if __name__ == "__main__":

    run(fshop_bottle, host=HOST_ADDRESS, port=HOST_PORT, reloader=AUTORELOAD)
