"""
"""

from bottle import view, abort, request, redirect
from formencode import validators, Schema


class FShopTabs(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle, auth, util):
        self._config = config
        self._FSDBsys = dbsys
        self._util = util
        self._auth = auth
        self._base_util = b_util

        fshop_bottle.get('/<tab_name:path>')(self.tab)

        fshop_bottle.post('/_sitefuncs_/edittab')(self.add_or_edit_tab)
        fshop_bottle.post('/_sitefuncs_/deletetab')(self.delete_tab)

        self._add_tab_sv = ["tab_name", "tab_rank"]

    #### View Routes ####
    @view('main')
    def tab(self, tab_name):

        tab = self._FSDBsys.route_db.get_tab_by_name(tab_name)
        if not tab:
            abort(404)
        pm = self._util.get_page_model(tab)
        return pm

    #### Edit Routes ####
    def add_or_edit_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form['selected_url']
        tab = form['tab_name']

        valid_req = self._base_util.validate_schema(AddEditTabSchema(), form, self._add_tab_sv)

    def add_tab(self):

        if self._FSDBsys.route_db.get_tab(tab):
            self._base_util.flash_alert("Could not add specified tab tab. One with that name already exists.", "alert-error", "Error")
            valid_req = False

        if valid_req:
            title = form.get('tab_title', None)
            desc = form.get('tab_desc', None)
            priority = form["tab_rank"]

            self._FSDBsys.route_db.add_new_tab(tab, priority, title, desc)
            self._FSDBsys.rank_db.new_tail_rank(tab)
            self._FSDBsys.rank_db.increment_tab_rank()

        redirect(selected_url)

    def edit_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form['selected_url']
        tab = form['tab_name']

        valid_req = self._base_util.validate_schema(AddtabSchema(), form, self._add_tab_sv)

        if self._FSDBsys.route_db.get_tab(tab):
            self._base_util.flash_alert("Could not edit specified tab tab. One with that name already exists.", "alert-error", "Error")
            valid_req = False

        if valid_req:
            title = form.get('tab_title', None)
            desc = form.get('tab_desc', None)
            priority = form["tab_rank"]
            tab_id = form['tab_id']

            self._FSDBsys.route_db.add_new_tab(tab, priority, title, desc)
            self._FSDBsys.rank_db.increment_tab_rank()

        redirect(selected_url)

    def delete_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form.get('selected_url', '/')
        tab = form['tab_name']

        if self._FSDBsys.route_db.get_tab(tab):
            self._FSDBsys.route_db.remove_tab(tab)
            self._FSDBsys.rank_db.remove_tail_rank(tab)
            self._FSDBsys.rank_db.increment_tab_rank(-1)

        redirect(selected_url)


class AddEditManeSchema(Schema):
    mane_name = validators.String(not_empty=True)
    mane_rank = validators.Int()
