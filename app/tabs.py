"""
"""

from bottle import request, redirect, jinja2_view as view
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

        self._add_tab_sv = ["tab_name", "tab_rank", "tab_ppp"]

    #### View Routes ####
    @view('jinja/main.jtml')
    def tab(self, tab_name):

        tab = self._FSDBsys.route_db.get_tab_by_name(tab_name)
        if not tab:
            redirect('/404')
        pm = self._util.get_page_model(tab)
        return pm

    #### Edit Routes ####
    def add_or_edit_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_tab = form['selected_tab']
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

        self._util.tab_redirect(selected_tab)

    def add_tab(self, form):
        name = form['tab_name']
        title = form.get('tab_title', None)
        desc = form.get('tab_desc', None)
        rank = form["tab_rank"]
        parent = form['tab_parent']
        ppp = int(form['tab_ppp'])
        nav_display = True

        self._FSDBsys.route_db.add_new_tab(name, rank, title, desc, parent, nav_display, ppp)

    def edit_tab(self, form):
        tab_id = form['tab_id']
        name = form['tab_name']
        title = form.get('tab_title', None)
        desc = form.get('tab_desc', None)
        rank = form["tab_rank"]
        parent = form['tab_parent']
        ppp = int(form['tab_ppp'])
        nav_display = True

        self._FSDBsys.route_db.edit_tab(tab_id, name, rank, title, desc, parent, nav_display, ppp)

    def delete_tab(self):
        self._auth.validate_session()
        form = request.forms
        selected_tab = form.get('selected_tab')
        tab_id = form['tab_id']
        tab = self._FSDBsys.route_db.get_tab(tab_id)

        if tab:
            self._util.remove_tab(tab['_id'])

        self._util.tab_redirect(selected_tab)


class AddEditTabSchema(Schema):
    tab_name = validators.String(not_empty=True)
    tab_rank = validators.Int()
    tab_ppp = validators.Int(min=1)
