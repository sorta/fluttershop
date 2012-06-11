import ConfigParser

DEF_CONF = {
    'host_address': '127.0.0.1',
    'host_port': '80',
    'autoreload': True,
    'debug': False,
    'server': 'auto',
    'mongo_address': '127.0.0.1',
    'mongo_port': 27017,
    'redis_address': '127.0.0.1',
    'redis_port': 6379,
    'sdb_key': None,
    'sdb_secret_key': None,
    'route_db': 'mongo',
    'content_db': 'mongo',
    'rank_db': 'mongo',
    'options_db': 'mongo'
}


class FShopConfig():

    def __init__(self, path='fshop.conf'):
        self._conf_path = path
        self.read_config_from_file(path)

    def read_config_from_file(self, path='fshop.conf'):
        conf = ConfigParser.RawConfigParser(DEF_CONF)
        conf.read(path)

        self._host_address = conf.get('general', 'host_address')
        self._host_port = conf.get('general', 'host_port')
        self._autoreload = conf.getboolean('general', 'autoreload')
        self._debug = conf.getboolean('general', 'debug')
        self._server = conf.get('general', 'server')

        self._mongo_address = conf.get('db', 'mongo_address')
        self._mongo_port = conf.getint('db', 'mongo_port')
        self._redis_address = conf.get('db', 'redis_address')
        self._redis_port = conf.getint('db', 'redis_port')
        self._sdb_key = conf.get('db', 'sdb_key')
        self._sdb_secret_key = conf.get('db', 'sdb_secret_key')
        self._route_db = conf.get('db', 'route_db')
        self._content_db = conf.get('db', 'content_db')
        self._rank_db = conf.get('db', 'rank_db')
        self._options_db = conf.get('db', 'options_db')

    @property
    def host_address(self):
        return self._host_address

    @property
    def host_port(self):
        return self._host_port

    @property
    def autoreload(self):
        return self._autoreload

    @property
    def debug(self):
        return self._debug

    @property
    def server(self):
        return self._server

    @property
    def mongo_address(self):
        return self._mongo_address

    @property
    def mongo_port(self):
        return self._mongo_port

    @property
    def redis_address(self):
        return self._redis_address

    @property
    def redis_port(self):
        return self._redis_port

    @property
    def sdb_key(self):
        return self._sdb_key

    @property
    def sdb_secret_key(self):
        return self._sdb_secret_key

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
