import random
from hashlib import sha512


class FShopCrypto(object):

    def __init__(self):
        self._ab = u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def generate_salt(self):
        return u''.join(random.choice(self._ab) for i in range(16))

    def generate_hash(self, password, salt):
        return unicode(sha512(salt + unicode(password)).hexdigest())

    def hash_password(self, password):
        salt = self.generate_salt()
        hashed_pass = self.generate_hash(password, salt)
        return hashed_pass, salt
