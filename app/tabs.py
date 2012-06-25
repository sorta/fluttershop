"""
"""

from bottle import view, abort, request, redirect


class FShopTabs(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle, auth, util):
        self._config = config
        self._FSDBsys = dbsys
        self._util = util
        self._auth = auth
        self._base_util = b_util

        fshop_bottle.get('/<mane_name>')(self.mane)
        fshop_bottle.get('/<mane_name>/<tail_name>')(self.tail)

        fshop_bottle.post('/_sitefuncs_/addmane')(self.add_mane)
        fshop_bottle.post('/_sitefuncs_/deletemane')(self.delete_mane)

        fshop_bottle.post('/_sitefuncs_/addtail')(self.add_tail)
        fshop_bottle.post('/_sitefuncs_/deletetail')(self.delete_tail)

    #### View Routes ####
    @view('main')
    def mane(self, mane_name):

        mane = self._FSDBsys.route_db.get_mane(mane_name)
        if not mane:
            abort(404)
        pm = self._util.get_page_model(mane)
        return pm

    @view('main')
    def tail(self, mane_name, tail_name):
        mane = self._FSDBsys.route_db.get_mane(mane_name)
        tail = self._FSDBsys.route_db.get_tail(mane_name, tail_name)

        if not mane or not tail:
            abort(404)
        pm = self._util.get_page_model(mane, tail)
        return pm

    #### Edit Routes ####
    def add_mane(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form['selected_url']
        mane = form['mane_name']

        if self._FSDBsys.route_db.get_mane(mane):
            self._base_util.flash_alert("Could not add specified mane tab. One with that name already exists.", "alert-error", "Operation Failed")
        else:
            title = form.get('mane_title', None)
            desc = form.get('mane_desc', None)
            priority = self._FSDBsys.rank_db.get_next_mane_rank()
            self._FSDBsys.route_db.add_new_mane(mane, priority, title, desc)
            self._FSDBsys.rank_db.increment_mane_rank()

        redirect(selected_url)

    def delete_mane(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form.get('selected_url', '/')
        mane = form['mane_name']

        if self._FSDBsys.route_db.get_mane(mane):
            self._FSDBsys.route_db.remove_mane(mane)
            self._FSDBsys.rank_db.increment_mane_rank(-1)

        redirect(selected_url)

    def add_tail(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form['selected_url']
        mane = form['selected_mane']
        tail = form['tail_name']

        if self._FSDBsys.route_db.get_tail(mane, tail):
            self._base_util.flash_alert("Could not add specified tail tab. One with that name already exists.", "alert-error", "Operation Failed")
        else:
            priority = self._FSDBsys.rank_db.get_next_tail_rank(mane)
            title = form.get('tail_title', None)
            desc = form.get('tail_desc', None)

            self._FSDBsys.route_db.add_new_tail(mane, tail, priority, title, desc)
            self._FSDBsys.rank_db.increment_tail_rank(mane)

        redirect(selected_url)

    def delete_tail(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form.get('selected_url', '/')
        mane = form['mane_name']
        tail = form['tail_name']

        if self._FSDBsys.route_db.get_tail(mane, tail):
            self._FSDBsys.route_db.remove_tail(mane, tail)
            self._FSDBsys.rank_db.increment_tail_rank(mane, -1)

        redirect(selected_url)
