from bottle import request, redirect


class FShopPost(object):
    def __init__(self, ptype, urlfield="post_url", atfield="post_alt_text", capfield="post_caption"):
        self._post_type = ptype
        self._body_field = "post_text"
        self._url_field = urlfield
        self._alt_text_field = atfield
        self._caption_field = capfield

    @property
    def post_type(self):
        return self._post_type

    @property
    def body_field(self):
        return self._body_field

    @property
    def url_field(self):
        return self._url_field

    @property
    def alt_text_field(self):
        return self._alt_text_field

    @property
    def caption_field(self):
        return self._caption_field


POST_TYPE_MAP = {
    'txt': FShopPost('txt'),
    'pic': FShopPost('pic', 'post_pic_url', 'post_pic_alt', 'post_pic_cap'),
    'lnk': FShopPost('lnk', 'post_link_url', 'post_link_alt', 'post_link_cap'),
    'vid': FShopPost('vid', 'post_vid_url', capfield='post_vid_cap')
}

ALIGN_SET = set(['Left', 'Right', 'Center'])


class FShopContent(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle, auth, util):
        self._config = config
        self._FSDBsys = dbsys
        self._auth = auth
        self._util = util
        self._base_util = b_util

        fshop_bottle.post('/_sitefuncs_/addpost')(self.add_post)

        fshop_bottle.post('/_sitefuncs_/editpost')(self.edit_post)

    def add_post(self):
        self._auth.validate_session()
        form = request.forms
        route = form["selected_url"]
        rob = form["selected_rob"]
        title = form["post_title"]
        alignment = form.get("post_alignment", "left")
        width = int(form.get("post_width", 12))
        show_title = self._util.parse_checkbox(form.get("post_show_title", False))
        show_date = self._util.parse_checkbox(form.get("post_show_date", False))
        content = form.get("post_content")
        try:
            post_rank = int(form["post_rank"])
        except ValueError:
            post_rank = self._FSDBsys.rank_db.get_next_post_rank(route)

        mane, tail = self._util.parse_route(route)

        if alignment in ALIGN_SET:
            alignment = alignment.lower()
        else:
            alignment = int(alignment)

        self._FSDBsys.content_db.insert_new_post(route, mane, alignment, width, title, post_rank, show_title, show_date, content, tail)
        self._FSDBsys.rank_db.increment_post_rank(route)

        redirect(route)

    def edit_post(self):
        self._auth.validate_session()
        form = request.forms
        route = form["selected_url"]
        title = form["post_title"]
        alignment = form.get("post_alignment", "left")
        width = int(form.get("post_width", 12))
        show_title = self._util.parse_checkbox(form.get("post_show_title", False))
        show_date = self._util.parse_checkbox(form.get("post_show_date", False))
        content = form.get("post_content")
        post_id = form['post_id']

        try:
            post_rank = int(form["post_rank"])
        except ValueError:
            post_rank = self._FSDBsys.rank_db.get_next_post_rank(route)

        if alignment in ALIGN_SET:
            alignment = alignment.lower()
        else:
            alignment = int(alignment)

        self._FSDBsys.content_db.update_post(post_id, route, alignment, width, title, post_rank, show_title, show_date, content)
        self._FSDBsys.rank_db.one_up_post_rank(route, post_rank)

        redirect(route)
