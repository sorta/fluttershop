from bottle import request, redirect


class FShopSiteOptions(object):

    def __init__(self, b_util, db, auth, crypto, fshop_bottle):
        self._FSDBSys = db
        self._auth = auth
        self._crypto = crypto
        self._base_util = b_util

        fshop_bottle.post("/_sitefuncs_/options")(self.modify_options)
        fshop_bottle.post("/_sitefuncs_/changepassword")(self.modify_password)

    def modify_options(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form["selected_url"]

        valid_user = self._auth.verify_login(form["current_username"], form["current_password"], selected_url)

        self._FSDBSys.options_db.modify_user(valid_user['username'], form["new_username"], form["new_email"])
        self._FSDBSys.options_db.modify_site_name(form["new_site_name"])

        redirect(selected_url)

    def modify_password(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form["selected_url"]

        valid_user = self._auth.verify_login(form["current_username"], form["current_password"], selected_url)

        new_pass = form["new_pass"]
        confirm_new_pass = form["confirm_new_pass"]
        if new_pass != confirm_new_pass:

            self._base_util.flash_alert("The new passwords did not match.", "alert-error", "Operation Failed")
            redirect(selected_url)

        self._FSDBSys.options_db.modify_password(valid_user["username"], new_pass)

        redirect(selected_url)
