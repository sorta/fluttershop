from bottle import request, redirect
from formencode import validators, Schema


class FShopSiteOptions(object):

    def __init__(self, b_util, db, auth, crypto, fshop_bottle):
        self._FSDBSys = db
        self._auth = auth
        self._crypto = crypto
        self._base_util = b_util

        self._mod_opts_sv = ['new_username', 'new_email', 'default_posts_per_page']
        self._pass_change_sv = ["new_password", "confirm_new_password"]

        fshop_bottle.post("/_sitefuncs_/options")(self.modify_options)
        fshop_bottle.post("/_sitefuncs_/changepassword")(self.modify_password)

    def modify_options(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form["selected_url"]

        valid_req = self._base_util.validate_schema(ModOptsSchema(), form, self._mod_opts_sv)
        valid_user = self._auth.verify_login(form["current_username"], form["current_password"], selected_url)

        if valid_req and valid_user:
            self._FSDBSys.options_db.modify_user(valid_user['username'], form["new_username"], form["new_email"])
            self._FSDBSys.options_db.modify_site_name(form["new_site_name"])
            self._FSDBSys.options_db.modify_def_ppp(form["default_posts_per_page"])

        redirect(selected_url)

    def modify_password(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form["selected_url"]

        valid_user = self._auth.verify_login(form["current_username"], form["current_password"], selected_url)

        valid_req = self._base_util.validate_schema(PassChangeSchema(), form, self._pass_change_sv)
        if valid_req:
            self._FSDBSys.options_db.modify_password(valid_user["username"], form["new_password"])
            self._base_util.flash_alert("Your password has been successfully changed.", "alert-success", "Password Changed")

        redirect(selected_url)


class ModOptsSchema(Schema):
    new_username = validators.String(not_empty=True)
    new_email = validators.Email()
    default_posts_per_page = validators.Int()


class PassChangeSchema(Schema):
    new_password = validators.String(min=6)
    confirm_new_password = validators.String(not_empty=True)
    chained_validators = [validators.FieldsMatch("confirm_new_password", "new_password")]
    allow_extra_fields = True
