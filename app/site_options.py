from bottle import request, redirect


class FShopSiteOptions(object):

    def __init__(self, db, auth, crypto, fshop_bottle):
        self._FSDBSys = db
        self._auth = auth
        self._crypto = crypto

        fshop_bottle.post("/_sitefuncs_/options")(self.modify_options)

    def modify_options(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form["selected_url"]

        valid_user = self._auth.verify_login(form["current_username"], form["current_password"], selected_url)

        self._FSDBSys.options_db.modify_user(valid_user['username'], form["new_username"], form["new_email"])
        self._FSDBSys.options_db.modify_site_name(form["new_site_name"])

        redirect(selected_url)
