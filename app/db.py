import boto


class FShopDB():

    def __init__(self, key=None, secret_key=None):
        self._sdb = self.connect_to_sdb(key, secret_key)

    def connect_to_sdb(self, key, secret_key):
        if key and secret_key:
            sdb = boto.connect_sdb(key, secret_key)
        else:
            sdb = boto.connect_sdb()

        return sdb

    def get_manelinks(self):
        manes = self._sdb.get_domain('ManeLink')

        links = []
        for item in manes:
            links.append([item['name'], item.name])

        return links

    def get_taillinks(self, mane):
        tails = self._sdb.get_domain('TailLink')
        narrowed = tails.select("select * from TailLink where mane_name = '{0}'".format(mane.lower()))

        links = []
        for tail in narrowed:
            links.append([tail['tail_name'], tail.name.replace('_', '/')])
        return links

    def get_links_for_mane(self, mane):
        manes = self.get_manelinks()
        tails = self.get_taillinks(mane.lower())
        return manes, tails

    def validate_mane(self, mane):
        manes = self._sdb.get_domain('ManeLink')
        return True if manes.get_item(mane.lower()) else False

    def validate_tail(self, mane, tail):
        tails = self._sdb.get_domain('TailLink')
        return True if tails.get_item('{0}_{1}'.format(mane.lower(), tail.lower())) else False
