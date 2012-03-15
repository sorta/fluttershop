import os
from bottle import run, get, route, static_file, error, redirect, view, template

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')


def build_app():

    run(host='localhost', port=8080, reloader=True)


@get('/')
def index():
    redirect("/home")


@get('/home')
@view('index')
def home():
    # output = template('index', data='Hello World!!!')
    # return output
    return dict(data='Hello World!!!')


@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=static_dir)


@error(404)
def error404(error):
    return 'Nothing here, sorry'


build_app()
