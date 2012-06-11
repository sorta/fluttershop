"""
"""

from bottle import request, redirect, abort


class FShopAuth(object):

    def __init__(self, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys

        fshop_bottle.post('/_sitefuncs_/login')(self.login)
        fshop_bottle.post('/_sitefuncs_/logout')(self.logout)

    #### User Routes ####
    def login(self):
        form = request.forms
        selected_url = form.get('selected_url', '/')

        user = self.verify_login(form.get('login_username', None), form.get('login_pass', None), selected_url)

        session = request.environ.get('beaker.session')
        session['logged_in'] = True
        session['user'] = user

        redirect(selected_url)

    def logout(self):
        session = request.environ.get('beaker.session')
        session['logged_in'] = False
        session['user'] = None

        redirect(request.forms.get('selected_url', '/'))

    def verify_login(self, user_id, password, selected_url):
        user = self._FSDBsys.options_db.get_user(user_id, password)
        if not user:
            redirect(selected_url)

        return user

    def validate_session(self):
        session = request.environ.get('beaker.session')
        logged_in = session.get('logged_in', False)
        user = session.get('user', {})
        if logged_in and self._FSDBsys.options_db.user_exists(user.get('username', None)):
            return True
        else:
            abort(401)
