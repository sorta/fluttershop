"""
"""

from bottle import view, abort, request, redirect


class FShopTabs(object):

    def __init__(self, config, dbsys, fshop_bottle, auth, util):
        self._config = config
        self._FSDBsys = dbsys
        self._util = util
        self._auth = auth

        fshop_bottle.get('/<mane>')(self.mane)
        fshop_bottle.get('/<mane>/<tail>')(self.tail)

        fshop_bottle.post('/addmane')(self.add_mane)
        fshop_bottle.post('/deletemane')(self.delete_mane)

        fshop_bottle.post('/addtail')(self.add_tail)

    #### View Routes ####
    @view('main')
    def mane(self, mane):
        if not self._FSDBsys.route_db.get_mane(mane):
            abort(404)
        pm = self._util.get_page_model(mane)
        return pm

    @view('main')
    def tail(self, mane, tail):
        if not self._FSDBsys.route_db.get_tail(mane, tail):
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
            # Flash Error!
            pass
        else:
            title = form.get('mane_title', None)
            desc = form.get('mane_desc', None)
            priority = self._FSDBsys.rank_db.get_next_mane_rank()
            self._FSDBsys.route_db.add_new_mane(mane, priority, title, desc)

        redirect(selected_url)

    def delete_mane(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form.get('selected_url', '/')
        mane = form['mane_name']

        if self._FSDBsys.route_db.get_mane(mane):
            self._FSDBsys.route_db.remove_mane(mane)

        redirect(selected_url)

    def add_tail(self):
        self._auth.validate_session()
        form = request.forms
        selected_url = form['selected_url']
        mane = form['selected_mane']
        tail = form['tail_name']

        if self._FSDBsys.route_db.get_tail(mane, tail):
            # Flash Error!
            pass
        else:
            priority = self._FSDBsys.rank_db.get_next_tail_rank(mane)
            self._FSDBsys.route_db.add_new_tail(mane, tail, priority)

        redirect(selected_url)
