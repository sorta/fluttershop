"""
"""

from bottle import request
from datetime import datetime
from math import ceil
from urlparse import urlparse, parse_qs


class FShopUtil(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys
        self._base_util = b_util

    #### Helpers ####
    def get_page_model(self, mane, tail=None):
        manes, tails = self._FSDBsys.route_db.get_links_for_mane(mane['mane_name'])
        site_name = self._FSDBsys.options_db.get_site_name()

        if tail:
            route = tail['route_name']
            page_title = tail['title']
            page_desc = tail['desc']
            tail_name = tail['tail_name']
        else:
            route = mane['route_name']
            page_title = mane['title']
            page_desc = mane['desc']
            tail_name = None

        rows = self.listify_posts(route)
        alerts = self.get_flash_alerts()

        return self.add_user_info({
            'manelinks': manes,
            'taillinks': tails,
            'selected_mane': mane['mane_name'],
            'selected_tail': tail_name,
            'page_title': page_title,
            'page_desc': page_desc,
            'site_name': site_name["site_name"],
            'rows': rows,
            'flash_alerts': alerts
        })

    def get_flash_alerts(self):
        session = request.environ.get('beaker.session')
        alerts = session.get('flash_alerts', [])
        session['flash_alerts'] = []
        return alerts

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
                        'url': part.get('url', u""),
                        'alt_text': part.get('alt_text', u""),
                        'caption': part.get('caption', u""),
                        'yt_id': part.get('yt_id', u""),
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


class FShopBaseUtil(object):

    def yt_video_id(self, url):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # fail?
        return None

    def flash_alert(self, message, msg_class=None, msg_title=None, session=None):

        if not session:
            session = request.environ.get('beaker.session')

        alerts = session.get('flash_alerts', [])
        new_alert = {
            'message': message,
        }

        if msg_title:
            new_alert['title'] = msg_title

        if msg_class:
            new_alert['msg_classes'] = msg_class

        alerts.append(new_alert)

        session['flash_alerts'] = alerts
