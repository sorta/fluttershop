
import redis


class FShopRedis():

    def __init__(self, server_address, server_port):

        self._r_server = redis.Redis(host=server_address, port=server_port)
