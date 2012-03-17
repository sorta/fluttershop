from boto import connect_sdb


class FShopSimpleDB():

    def __init__(self, key=None, secret_key=None):
        self._sdb = self.connect_to_sdb(key, secret_key)

    def connect_to_sdb(self, key, secret_key):
        if key and secret_key:
            sdb = connect_sdb(key, secret_key)
        else:
            sdb = connect_sdb()

        return sdb

    def get_manelinks(self):
        return self._sdb.get_domain('ManeLink')

    def get_taillinks(self, mane):
        tails = self._sdb.get_domain('TailLink')
        return tails.select("select * from `TailLink` where mane_name = '{0}'".format(mane.lower()))

    def get_links_for_mane(self, mane):
        manes = self.get_manelinks()
        tails = self.get_taillinks(mane.lower())
        return manes, tails

    def get_mane_mane(self):
        manes = self._sdb.get_domain('ManeLink')
        result = manes.select("select * from `ManeLink` where priority >= '0' order by priority limit 1")

        try:
            mane = result.next()
            return mane.name
        except StopIteration:
            return "bc"

    def validate_mane(self, mane):
        manes = self._sdb.get_domain('ManeLink')
        return True if manes.get_item(mane.lower()) else False

    def validate_tail(self, mane, tail):
        tails = self._sdb.get_domain('TailLink')
        return True if tails.get_item('{0}/{1}'.format(mane.lower(), tail.lower())) else False
