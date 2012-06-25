
FSM = None
FSS = None
FSR = None


def get_db_sys(name, b_util, config, crypto):
    if name == 'mongo':
        global FSM
        if FSM is None:
            from app.db_imps.fs_mongo import FShopMongoDB
            FSM = FShopMongoDB(b_util, crypto, config)
        return FSM

    if name == 'sdb':
        global FSS
        if FSS is None:
            from db_imps.fs_sdb import FShopSimpleDB
            FSS = FShopSimpleDB(b_util, crypto, config)
        return FSS

    if name == 'redis':
        global FSR
        if FSR is None:
            from app.db_imps.fs_redis import FShopRedis
            FSR = FShopRedis(b_util, crypto, config)
        return FSR


class FShopDBSys(object):

    def __init__(self, b_util, config, crypto):

        self._route_db = get_db_sys(config.route_db, b_util, config, crypto)
        self._content_db = get_db_sys(config.content_db, b_util, config, crypto)
        self._rank_db = get_db_sys(config.rank_db, b_util, config, crypto)
        self._options_db = get_db_sys(config.options_db, b_util, config, crypto)

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
