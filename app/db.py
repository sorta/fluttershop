
FSM = None
FSS = None
FSR = None


def get_db_sys(name, config, crypto):
    if name == 'mongo':
        global FSM
        if FSM is None:
            from app.db_imps.fs_mongo import FShopMongoDB
            FSM = FShopMongoDB(crypto, config.mongo_address, config.mongo_port)
        return FSM

    if name == 'sdb':
        global FSS
        if FSS is None:
            from db_imps.fs_sdb import FShopSimpleDB
            FSS = FShopSimpleDB(crypto, config.sdb_key, config.sdb_secret_key)
        return FSS

    if name == 'redis':
        global FSR
        if FSR is None:
            from app.db_imps.fs_redis import FShopRedis
            FSR = FShopRedis(crypto, config.redis_address, config.redis_port)
        return FSR


class FShopDBSys(object):

    def __init__(self, config, crypto):

        self._route_db = get_db_sys(config.route_db, config, crypto)
        self._content_db = get_db_sys(config.content_db, config, crypto)
        self._rank_db = get_db_sys(config.rank_db, config, crypto)
        self._options_db = get_db_sys(config.options_db, config, crypto)

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
