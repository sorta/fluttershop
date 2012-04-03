from hashlib import sha512

connect_sdb = None
pymongo = None
redis = None

FSM = None
FSS = None
FSR = None


def get_db_sys(name, config):
    if name == 'mongo':
        global FSM
        if FSM is None:
            FSM = FShopMongoDB(config.mongo_address, config.mongo_port)
        return FSM

    if name == 'sdb':
        global FSS
        if FSS is None:
            FSS = FShopSimpleDB(config.sdb_key, config.sdb_secret_key)
        return FSS

    if name == 'redis':
        global FSR
        if FSR is None:
            FSR = FShopRedis(config.redis_address, config.redis_port)
        return FSR


class FShopDBSys(object):

    def __init__(self, config):

        self._route_db = get_db_sys(config.route_db, config)
        self._content_db = get_db_sys(config.content_db, config)
        self._rank_db = get_db_sys(config.rank_db, config)
        self._options_db = get_db_sys(config.options_db, config)

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
    def options_db(self):
        return self._options_db


class IFShopDB(object):

    #### CONTENT ####
    def get_parts_for_post(self, post_id):
        return

    def get_posts_for_route(self, route_id, post_limit=10):
        return

    #### OPTIONS ####

    #### RANKING ####

    #### ROUTING ####
    def add_new_mane(self, mane):
        return

    def get_manelinks(self):
        return

    def get_taillinks(self, mane):
        return

    def get_links_for_mane(self, mane):
        return

    def get_mane_mane(self):
        return

    def validate_mane(self, mane):
        return

    def validate_tail(self, mane, tail):
        return


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

    @property
    def options_collection(self):
        return self._mdb.options

    @property
    def ranks_collection(self):
        return self._mdb.ranks

    @property
    def routes_collection(self):
        return self._mdb.routes

    #### CONTENT ####
    def get_parts_for_post(self, post_id):
        part_col = self.parts_collection
        return part_col.find({'post_id': post_id}).sort('rank', 1)

    def get_posts_for_route(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': unicode(route_id)}).sort('rank', 1).limit(post_limit)

    #### OPTIONS ####
    def get_user(self, username, password):
        prepared_pass = unicode(sha512(u'KsdfKSDFGT435Jwef45TJ6' + unicode(password)).hexdigest())
        return self.options_collection.find_one({'username': username, 'password': prepared_pass})

    def user_exists(self, username):
        return self.options_collection.find_one({'username': username})

    #### RANKING ####
    def get_next_rank(self, rank_type):
        return self.ranks_collection.find_one({'rank_type': rank_type}, fields=['next_rank'])

    def increment_rank(self, rank_type, incr_value=1):
        self.ranks_collection.update({'rank_type': rank_type}, {'$inc': {'next_rank': incr_value}})

    #### ROUTING ####
    def add_new_mane(self, mane_name, priority):
        next_rank = self.get_next_rank('mane')
        manes = self.get_manelinks()
        for mane in manes:
            if True:
                pass
        return

    def remove_mane(self, mane_name):
        return

    def get_manelinks(self):
        return self.routes_collection.find({'route_type': 'mane'}).sort('rank', 1)

    def get_taillinks(self, mane):
        return

    def get_links_for_mane(self, mane):
        return

    def get_mane_mane(self):
        return

    def validate_mane(self, mane):
        return

    def validate_tail(self, mane, tail):
        return


class FShopRedis():

    def __init__(self, server_address, server_port):
        global redis
        if redis is None:
            import redis

        self._r_server = redis.Redis(host=server_address, port=server_port)
