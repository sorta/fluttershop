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

    def add_post(self):
        self._auth.validate_session()
        form = request.forms
        route = form["selected_url"]
        title = form["post_title"]
        alignment = form.get("post_alignment", "left")
        width = int(form.get("post_width", 12))
        post_type = form["sel_post_type"]
        show_title = self._util.parse_checkbox(form.get("post_show_title", False))
        show_date = self._util.parse_checkbox(form.get("post_show_date", False))
        mane, tail = self._util.parse_route(route)
        next_post_rank = self._FSDBsys.rank_db.get_next_post_rank(route)

        if alignment in ALIGN_SET:
            alignment = alignment.lower()
        else:
            alignment = int(alignment)

        post_id = self._FSDBsys.content_db.insert_new_post(route, mane, post_type, alignment, width, title, next_post_rank, show_title, show_date, tail)
        self._FSDBsys.rank_db.increment_post_rank(route)

        post_fields = POST_TYPE_MAP.get(post_type)
        body = form.get(post_fields.body_field)
        url = form.get(post_fields.url_field, None)
        alt_text = form.get(post_fields.alt_text_field, None)
        caption = form.get(post_fields.caption_field, None)
        next_part_rank = self._FSDBsys.rank_db.get_next_post_part_rank(post_id)

        self._FSDBsys.content_db.insert_new_post_part(post_id, post_type, body, next_part_rank, alt_text, caption, url)
        self._FSDBsys.rank_db.increment_post_part_rank(post_id)

        redirect(route)
