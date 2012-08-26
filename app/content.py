from bottle import request
from formencode import validators, Schema

ALIGN_SET = set(['Left', 'Right', 'Center'])


class FShopContent(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle, auth, util):
        self._config = config
        self._FSDBsys = dbsys
        self._auth = auth
        self._util = util
        self._base_util = b_util
        self._edit_post_sv = ['post_content', 'post_rank']

        fshop_bottle.post('/_sitefuncs_/editpost')(self.add_or_edit_post)
        fshop_bottle.post('/_sitefuncs_/deletepost')(self.delete_post)

    def get_rank_from_form(self, form, tab_id):

        try:
            post_rank = int(form["post_rank"])
        except ValueError:
            post_rank = self._FSDBsys.content_db.get_next_post_rank(tab_id)

        return post_rank

    def add_or_edit_post(self):
        self._auth.validate_session()
        form = request.forms
        action = form['post_action']
        title = form["post_title"]
        alignment = form.get("post_alignment", "left")
        width = int(form.get("post_width", 12))
        show_title = self._util.parse_checkbox(form.get("post_showtitle", False))
        show_date = self._util.parse_checkbox(form.get("post_showdate", False))
        content = form.get("post_content")
        selected_tab = form["selected_tab"]

        if alignment in ALIGN_SET:
            alignment = alignment.lower()
        else:
            alignment = int(alignment)

        valid_req = self._base_util.validate_schema(PostSchema(), form, self._edit_post_sv)

        if valid_req:
            if action == 'add':
                rank = self.get_rank_from_form(form, selected_tab)
                self._FSDBsys.content_db.insert_new_post(selected_tab, alignment, width, title, rank, show_title, show_date, content)

            elif action == 'edit':
                post_id = form['post_id']
                tab_id = form.get('tab_id', None)
                rank = self.get_rank_from_form(form, tab_id)
                self._FSDBsys.content_db.update_post(post_id, tab_id, alignment, width, title, rank, show_title, show_date, content)

        self._util.tab_redirect(selected_tab)

    def delete_post(self):
        self._auth.validate_session()
        form = request.forms
        selected_tab = form.get('selected_tab')
        post_id = form['post_id']
        post = self._FSDBsys.content_db.get_post(post_id)

        if post:
            self._FSDBsys.content_db.remove_post(post['_id'])

        self._util.tab_redirect(selected_tab)


class PostSchema(Schema):
    post_content = validators.String(not_empty=True)
    post_rank = validators.Int()
