import os
from bottle import run, Bottle, redirect, static_file

from config import HOST_ADDRESS, HOST_PORT, AUTORELOAD, my_view
from db import get_manelinks, get_taillinks

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
fshop_bottle = Bottle()


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
@my_view('index')
def mane():
    manelinks = get_manelinks()
    taillinks = get_taillinks()
    return dict(data='Hello World!!!', manelinks=manelinks, taillinks=taillinks)


@fshop_bottle.get('/<mane>/<tail>')
@my_view('index')
def tail():
    manelinks = get_manelinks()
    taillinks = get_taillinks(mane)
    return dict(data='Hello World!!!', manelinks=manelinks, taillinks=taillinks)

#### Main ####
if __name__ == "__main__":

    run(fshop_bottle, host=HOST_ADDRESS, port=HOST_PORT, reloader=AUTORELOAD)
