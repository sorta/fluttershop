
from boto import connect_sdb


class FShopSimpleDB():

    def __init__(self, key=None, secret_key=None):
        if key and secret_key:
            self._sdb = connect_sdb(key, secret_key)
        else:
            self._sdb = connect_sdb()

    #### CONTENT ####
    #TODO: Implement these!

    #### OPTIONS ####
    #TODO: Implement these!

    #### RANKING ####
    #TODO: Implement these!

    #### Routing ####
    def add_new_mane(self, mane_name, priority):
        manes = self.get_manelinks()
        new_mane = manes.new_item(mane_name.lower())
        new_mane['mane_name'] = mane_name
        new_mane['priority'] = priority
        new_mane.save()

    def remove_mane(self, mane_name):
        manes = self.get_manelinks()
        result = manes.select("select * from `ManeLink` where priority >= '0' order by priority")
        decrement = False
        for mane in result:
            if mane['mane_name'] == mane_name:
                decrement = True
                manes.delete_item(mane)
                continue
            if decrement:
                mane['priority'] = int(mane['priority']) - 1

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
