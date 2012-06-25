"""
"""

from bottle import request, redirect, abort


class FShopAuth(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys
        self._base_util = b_util

        fshop_bottle.post('/_sitefuncs_/login')(self.login)
        fshop_bottle.post('/_sitefuncs_/logout')(self.logout)

    #### User Routes ####
    def login(self):
        form = request.forms
        selected_url = form.get('selected_url', '/')

        user = self._FSDBsys.options_db.get_user_check_password(form.get('login_username', None), form.get('login_pass', None))
        if not user:
            self._base_util.flash_alert("Login Failed. The username or password did not match.", "alert-error", "Login Failed")
            redirect(selected_url)

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
        user = self._FSDBsys.options_db.get_user_check_password(user_id, password)
        if not user:
            self._base_util.flash_alert("Authentication Failed. The password did not match.", "alert-error", "Authentication Failed")

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
