"""
"""

from bottle import request, redirect
from datetime import datetime
from math import ceil
from urlparse import urlparse, parse_qs
from formencode import Invalid
from string import capwords


class FShopUtil(object):

    def __init__(self, b_util, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys
        self._base_util = b_util

    #### Helpers ####
    def get_page_model(self, tab):
        tabs = self._FSDBsys.route_db.get_tab_links(tab['_id'], tab.get('parent', None))
        site_name = self._FSDBsys.options_db.get_site_name()

        rows = self.listify_posts(tab)
        alerts = self.get_flash_alerts()

        pm = self.add_user_info({
            'tabs': tabs,
            'selected_tab': tab,
            'page_title': tab.get('title', None),
            'page_desc': tab.get('desc', None),
            'site_name': site_name["site_name"],
            'rows': rows,
            'flash_alerts': alerts
        })

        if pm['logged_in']:
            pm['def_ppp'] = self._FSDBsys.options_db.get_def_ppp()
            pm['next_post_rank'] = self._FSDBsys.content_db.get_next_post_rank(tab['_id'])

        return pm

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

    def get_width_str(self, h_loc, requested, alignment, new_row=False):
        if h_loc + requested > 12:
            h_loc = 0
            return self.get_width_str(h_loc, requested, alignment, True)

        if alignment == u'left':
            h_loc += requested
            return new_row, h_loc, requested, 0

        if alignment == u'right':
            offset = 12 - h_loc - requested
            h_loc = 12
            return new_row, h_loc, requested, offset

        if alignment == u'center':
            remainder = 12 - h_loc
            offset = int(ceil((remainder - requested) / 2))
            h_loc += requested + offset
            return new_row, h_loc, requested, offset

        if alignment > 0 and alignment < 12:

            if requested + alignment > 12:
                alignment = 12 - requested

            if h_loc + requested + alignment > 12:
                return self.get_width_str(h_loc, requested, alignment, True)

            return new_row, h_loc, requested, alignment

    def listify_posts(self, tab):
        posts = self._FSDBsys.content_db.get_posts_for_tab(tab['_id'], post_limit=10)

        post_list = []
        rows = []
        h_loc = 0

        for post in posts:

            requested = post.get('width', 12)
            alignment = post.get('alignment', u'left')
            new_row, h_loc, width, offset = self.get_width_str(h_loc, requested, alignment)

            if new_row:
                rows.append(post_list)
                post_list = []

            post['offset'] = offset

            post_list.append(post)

        if len(post_list) > 0:
            rows.append(post_list)

        return rows

    def remove_tab(self, tab_id):
        self._FSDBsys.route_db.remove_tab(tab_id)
        self._FSDBsys.content_db.remove_posts_for_tab(tab_id)
        for route in self._FSDBsys.route_db.get_tabs_by_parent(tab_id):
            self.remove_tab(route['_id'])

    def parse_checkbox(self, data):
        if data == "on":
            return True
        return False

    def tab_redirect(self, tab_id):
        tab = self._FSDBsys.route_db.get_tab(tab_id)
        if tab:
            redirect(tab['path'])
        else:
            redirect('/')


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

    def clean_name(self, name):
        return unicode(name.lower().replace(" ", "_"))

    def pathify_name(self, name, is_clean=False):

        if not is_clean:
            name = self.clean_name(name)

        if name.startswith('/'):
            return name
        else:
            return u'/{0}'.format(name)

    def run_validator(self, validator, value):
        try:
            resp = validator.to_python(value)
            return True, resp
        except Invalid, e:
            return False, e

    def validate_schema(self, schema, form, vals):
        val_dict = dict(self.populate_val_dict(form, vals))
        response, val = self.run_validator(schema, val_dict)
        if not response:
            error_dict = val.error_dict
            if error_dict:
                for error in error_dict:
                    pez = capwords(error.replace("_", " "))
                    self.flash_alert("{0}: {1}".format(pez, error_dict[error]), 'alert-error', 'Error')
            return False
        return True

    def populate_val_dict(self, form, vals):
        for val in vals:
            yield val, form[val]
