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
        tab_name = form['tab_name']
        action = form['action']

        valid_req = self._base_util.validate_schema(AddEditTabSchema(), form, self._add_tab_sv)

        if action == 'add':
            if self._FSDBsys.route_db.get_tab_by_name(tab_name):
                self._base_util.flash_alert("Could not add specified tab. One with that name already exists.", "alert-error", "Error")
                valid_req = False

            if valid_req:
                self.add_tab(form)
        elif action == 'edit':
            tab_id = form['tab_id']
            tbn = self._FSDBsys.route_db.get_tab_by_name(tab_name)
            tbi = self._FSDBsys.route_db.get_tab(tab_id)
            if tbn and tbi and (tbn['_id'] != tbi['_id']):
                self._base_util.flash_alert("Could not edit specified tab. One with that name already exists.", "alert-error", "Error")
                valid_req = False

            if valid_req:
                self.edit_tab(form)

        redirect(selected_url)

    def add_tab(self, form):
        name = form['tab_name']
        title = form.get('tab_title', None)
        desc = form.get('tab_desc', None)
        rank = form["tab_rank"]
        parent = form['tab_parent']
        nav_display = True

        self._FSDBsys.route_db.add_new_tab(name, rank, title, desc, parent, nav_display)

    def edit_tab(self, form):
        tab_id = form['tab_id']
        name = form['tab_name']
        title = form.get('tab_title', None)
        desc = form.get('tab_desc', None)
        rank = form["tab_rank"]
        parent = form['tab_parent']
        nav_display = True

        self._FSDBsys.route_db.edit_tab(tab_id, name, rank, title, desc, parent, nav_display)

    def delete_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form.get('selected_url', '/')
        tab_name = form['tab_name']
        tab = self._FSDBsys.route_db.get_tab_by_name(tab_name)

        if tab:
            self._FSDBsys.route_db.remove_tab(tab['_id'])

        redirect(selected_url)


class AddEditTabSchema(Schema):
    tab_name = validators.String(not_empty=True)
    tab_rank = validators.Int()
