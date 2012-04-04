"""
"""

from bottle import request
from app.content import listify_posts


class FShopUtil(object):

    def __init__(self, config, dbsys, fshop_bottle):
        self._config = config
        self._FSDBsys = dbsys

    #### Helpers ####
    def get_page_model(self, mane, tail=None):
        manes, tails = self._FSDBsys.route_db.get_links_for_mane(mane)

        route = u"/{0}/{1}".format(mane, tail) if tail else u"/{0}".format(mane)
        rows = listify_posts(self._FSDBsys.content_db, route)
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
