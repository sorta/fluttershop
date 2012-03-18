connect_sdb = None
pymongo = None


class FShopDBSys():

    def __init__(self, load_mongo=True, load_simpledb=True, mongo_address='127.0.0.1', mongo_port=27017):

        if load_simpledb:
            self._simpledb = FShopSimpleDB()

        if load_mongo:
            self._mongo = FShopMongoDB(mongo_address, mongo_port)

    @property
    def mongo(self):
        return self._mongo

    @property
    def sdb(self):
        return self._simpledb


class FShopSimpleDB():

    def __init__(self, key=None, secret_key=None):
        global connect_sdb
        if connect_sdb is None:
            from boto import connect_sdb

        if key and secret_key:
            self._sdb = connect_sdb(key, secret_key)
        else:
            self._sdb = connect_sdb()

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


class FShopMongoDB():

    def __init__(self, db_address, db_port=27017):
        global pymongo
        if pymongo is None:
            import pymongo
        self._connection = pymongo.Connection(db_address, db_port)
        self._mdb = self._connection.fluttershop

    @property
    def posts_collection(self):
        return self._mdb.posts

    @property
    def parts_collection(self):
        return self._mdb.postparts

    def get_parts_for_post(self, post_id):
        part_col = self.parts_collection
        return part_col.find({'post_id': post_id}).sort('rank', 1)

    def get_posts_for_route(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': unicode(route_id)}).sort('rank', 1).limit(post_limit)

    def get_manelinks(self):
        pass

    def get_taillinks(self, mane):
        pass

    def get_links_for_mane(self, mane):
        pass

    def get_mane_mane(self):
        pass

    def validate_mane(self, mane):
        pass

    def validate_tail(self, mane, tail):
        pass
