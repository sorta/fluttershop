connect_sdb = None
pymongo = None
redis = None

FSM = None
FSS = None
FSR = None


def get_db_sys(name, config):
    if name == u'mongo':
        global FSM
        if FSM is None:
            FSM = FShopMongoDB(config.get('mongo_address', '127.0.0.1'), config.get('mongo_port', 27017))
        return FSM

    if name == u'sdb':
        global FSS
        if FSS is None:
            FSS = FShopSimpleDB(config.get('sdb_key', None), config.get('sdb_secret_key', None))
        return FSS

    if name == u'redis':
        global FSR
        if FSR is None:
            FSR = FShopRedis(config.get('redis_address', '127.0.0.1'), config.get('redis_port', 6379))
        return FSR


class FShopDBSys():

    def __init__(self, route_db, content_db, rank_db, user_db, config={}):

        self._route_db = get_db_sys(route_db, config)
        self._content_db = get_db_sys(content_db, config)
        self._rank_db = get_db_sys(rank_db, config)
        self._user_db = get_db_sys(user_db, config)

    @property
    def route_db(self):
        return self._route_db

    @property
    def content_db(self):
        return self._content_db

    @property
    def rank_db(self):
        return self._rank_db

    @property
    def user_db(self):
        return self._user_db


class FShopSimpleDB():

    def __init__(self, key=None, secret_key=None):
        global connect_sdb
        if connect_sdb is None:
            from boto import connect_sdb

        if key and secret_key:
            self._sdb = connect_sdb(key, secret_key)
        else:
            self._sdb = connect_sdb()

    #### CONTENT ####
    #TODO: Implement these!

    #### RANKING ####
    #TODO: Implement these!

    #### Routing ####
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

    #### USER ####
    #TODO: Implement these!


class FShopMongoDB():

    def __init__(self, db_address, db_port=27017):
        global pymongo
        if pymongo is None:
            import pymongo
        self._connection = pymongo.Connection(db_address, db_port)
        self._mdb = self._connection.fluttershop

    #### Collections ###
    @property
    def posts_collection(self):
        return self._mdb.posts

    @property
    def parts_collection(self):
        return self._mdb.postparts

    #### CONTENT ####
    def get_parts_for_post(self, post_id):
        part_col = self.parts_collection
        return part_col.find({'post_id': post_id}).sort('rank', 1)

    def get_posts_for_route(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': unicode(route_id)}).sort('rank', 1).limit(post_limit)

    #### RANKING ####
    #TODO: Implement these!

    #### ROUTING ####
    #TODO: Implement these!
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

    #### USER ####
    #TODO: Implement these!


class FShopRedis():

    def __init__(self, server_address, server_port):
        global redis
        if redis is None:
            import redis

        self._r_server = redis.Redis(host=server_address, port=server_port)
