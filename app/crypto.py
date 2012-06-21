import random
from hashlib import sha512
from urlparse import urlparse, parse_qs


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

    def yt_video_id(self, url):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # fail?
        return None
