from datetime import datetime
from math import ceil
from bottle import request


class FShopContent(object):

    def __init__(self, config, dbsys, fshop_bottle, auth):
        self._config = config
        self._FSDBsys = dbsys
        self._auth = auth

        fshop_bottle.post('/addpost')(self.add_post)

    def add_post(self):
        self._auth.validate_session()
        form = request.forms


def get_width_str(h_loc, requested, alignment, new_row=False):
    if h_loc + requested > 12:
        h_loc = 0
        return get_width_str(h_loc, requested, alignment, True)

    if alignment == u'left':
        h_loc += requested
        return new_row, h_loc, requested, 0

    if alignment == u'right':
        offset = 12 - h_loc - requested
        # width = "span{0} offset{1}".format(requested, offset) if offset > 0 else "span{0}".format(requested)
        h_loc = 12
        return new_row, h_loc, requested, offset

    if alignment == u'center':
        remainder = 12 - h_loc
        offset = int(ceil((remainder - requested) / 2))
        h_loc += requested + offset
        # width = "span{0} offset{1}".format(requested, offset) if offset > 0 else "span{0}".format(requested)
        return new_row, h_loc, requested, offset


def listify_posts(fshop_db, route_id):
    posts = fshop_db.get_posts_for_route(route_id, 10)

    post_list = []
    rows = []
    h_loc = 0

    for post in posts:
        part_list = []
        parts = fshop_db.get_parts_for_post(post['_id'])
        for part in parts:
            part_list.append({
                    'part_type': part.get('part_type', u'text'),
                    'body': part.get('body', u""),
                    'alt_text': part.get('alt_text', u""),
                    'caption': part.get('caption', u"")
                })

        requested = post.get('width', 12)
        alignment = post.get('alignment', u'left')
        new_row, h_loc, width, offset = get_width_str(h_loc, requested, alignment)

        if new_row:
            rows.append(post_list)
            post_list = []

        post_list.append({
                'post_type': post.get('post_type', u'text'),
                'title': post.get('title', u""),
                'date': post.get('timestamp', datetime.now()),
                'width': width,
                'offset': offset,
                'parts': part_list
            })

    if len(post_list) > 0:
        rows.append(post_list)

    return rows
