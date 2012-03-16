import boto


class FShopDB():

    def __init__(self, key=None, secret_key=None):
        self._sdb = self.connect_to_sdb(key, secret_key)

    def get_manelinks(self, key=None, secret_key=None):
        manes = self._sdb.get_domain('ManeLink')

        links = []
        for item in manes:
            links.append([item['name'], item.name])

        return links

    def get_taillinks(self, mane, key=None, secret_key=None):
        tails = self._sdb.get_domain('TailLink')
        narrowed = tails.select("select * from TailLink where mane_name = '{0}'".format(mane))

        links = []
        for tail in narrowed:
            links.append([tail['tail_name'], tail.name.replace('_', '/')])
        return links

    def connect_to_sdb(self, key, secret_key):
        if key and secret_key:
            sdb = boto.connect_sdb(key, secret_key)
        else:
            sdb = boto.connect_sdb()

        return sdb

    def validate_mane(mane):
        pass
