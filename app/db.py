
FSM = None
FSS = None
FSR = None


def get_db_sys(name, config):
    if name == 'mongo':
        global FSM
        if FSM is None:
            from app.db_imps.fs_mongo import FShopMongoDB
            FSM = FShopMongoDB(config.mongo_address, config.mongo_port)
        return FSM

    if name == 'sdb':
        global FSS
        if FSS is None:
            from db_imps.fs_sdb import FShopSimpleDB
            FSS = FShopSimpleDB(config.sdb_key, config.sdb_secret_key)
        return FSS

    if name == 'redis':
        global FSR
        if FSR is None:
            from app.db_imps.fs_redis import FShopRedis
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
