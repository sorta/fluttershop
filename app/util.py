"""
"""

from bottle import request
from datetime import datetime
from math import ceil


class FShopUtil(object):

    def __init__(self, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys

    #### Helpers ####
    def get_page_model(self, mane, tail=None):
        manes, tails = self._FSDBsys.route_db.get_links_for_mane(mane)

        route = u"/{0}/{1}".format(mane, tail) if tail else u"/{0}".format(mane)
        rows = self.listify_posts(route)
        return self.add_user_info({
            'manelinks': manes,
            'taillinks': tails,
            'selected_mane': mane,
            'selected_tail': tail,
            'site_name': self._config.site_name,
            'rows': rows
        })

    def add_user_info(self, pm):
        session = request.environ.get('beaker.session')
        pm['logged_in'] = session.get('logged_in', False)
        if pm['logged_in']:
            pm['user'] = session.get('user', None)
        return pm

    def parse_route(self, route):
        if route == "/":
            return None, None

        mane = None
        tail = None
        sprout = route.split('/')
        sprout_len = len(sprout)

        if sprout_len > 1:
            mane = sprout[1].lower()

            if sprout_len > 2:
                tail = sprout[2].lower()

        return mane, tail

    def get_width_str(self, h_loc, requested, alignment, new_row=False):
        if h_loc + requested > 12:
            h_loc = 0
            return self.get_width_str(h_loc, requested, alignment, True)

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

        if alignment > 0 and alignment < 12:

            if requested + alignment > 12:
                alignment = 12 - requested

            if h_loc + requested + alignment > 12:
                return self.get_width_str(h_loc, requested, alignment, True)

            return new_row, h_loc, requested, alignment

    def listify_posts(self, route_id):
        posts = self._FSDBsys.content_db.get_posts_for_route(route_id, 10)

        post_list = []
        rows = []
        h_loc = 0

        for post in posts:
            part_list = []
            parts = self._FSDBsys.content_db.get_parts_for_post(post['_id'])
            for part in parts:
                part_list.append({
                        'part_type': part.get('part_type', u'text'),
                        'part_id': part['_id'],
                        'body': part.get('body', u""),
                        'alt_text': part.get('alt_text', u""),
                        'caption': part.get('caption', u"")
                    })

            requested = post.get('width', 12)
            alignment = post.get('alignment', u'left')
            new_row, h_loc, width, offset = self.get_width_str(h_loc, requested, alignment)

            if new_row:
                rows.append(post_list)
                post_list = []

            post_list.append({
                    'post_type': post.get('post_type', u'txt'),
                    'post_id': post['_id'],
                    'title': post.get('title', u""),
                    'timestamp': post.get('timestamp', datetime.now()),
                    'date_created': post.get('date_created', datetime.now()),
                    'show_title': post['show_title'],
                    'show_date': post['show_date'],
                    'width': width,
                    'offset': offset,
                    'parts': part_list
                })

        if len(post_list) > 0:
            rows.append(post_list)

        return rows

    def parse_checkbox(self, data):
        if data == "on":
            return True
        return False
