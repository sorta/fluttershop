from datetime import datetime
import pymongo


class FShopMongoDB():

    def __init__(self, b_util, crypto, config):
        self._connection = pymongo.Connection(config.mongo_address, config.mongo_port)
        self._mdb = self._connection[config.deployment]
        self._base_util = b_util
        self._crypto = crypto

    #### Collections ###
    @property
    def posts_collection(self):
        return self._mdb.posts

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

    def get_posts_for_route(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': unicode(route_id).lower()}).sort('rank', -1).limit(post_limit)

    def insert_new_post(self, route, mane, alignment, width, title, next_rank, show_title, show_date, post_content, tail=None):
        post_col = self.posts_collection
        timestamp = datetime.now()
        new_post = {
            "route_id": route,
            "mane_id": mane,
            "post_content": post_content,
            "alignment": alignment,
            "width": width,
            "title": title,
            "show_title": show_title,
            "show_date": show_date,
            "date_created": timestamp,
            "date_modified": timestamp,
            "rank": next_rank
        }

        if tail:
            new_post["tail_id"] = tail

        return post_col.insert(new_post)

    #### OPTIONS ####
    def get_user_check_password(self, username, test_password):
        user = self.get_user(username)
        if not user:
            return None
        prepared_pass = self._crypto.generate_hash(test_password, user['salt'])
        return self.options_collection.find_one({'username': username, 'password': prepared_pass})

    def get_user(self, username):
        return self.options_collection.find_one({'username': username})

    def user_exists(self, username):
        user = self.get_user(username)
        if user:
            return True
        else:
            return False

    def at_least_one_user(self):
        item = self.options_collection.find_one({"option_type": "user"})
        if item:
            return True
        else:
            return False

    def _add_user(self, username, password, email):
        timestamp = datetime.now()
        hashed_pass, salt = self._crypto.hash_password(password)
        new_user = {
            "option_type": "user",
            "username": unicode(username),
            "email": email,
            "salt": salt,
            "password": hashed_pass,
            "date_created": timestamp,
            "date_modified": timestamp,
            "password_modified": timestamp,
        }
        self.options_collection.insert(new_user)

    def modify_user(self, current_username, new_username, new_email):
        timestamp = datetime.now()
        update = {
            "username": new_username,
            "email": new_email,
            "date_modified": timestamp
        }
        self.options_collection.update({"option_type": "user", "username": current_username}, {"$set": update})

    def modify_password(self, current_username, new_password):
        timestamp = datetime.now()
        hashed_pass, salt = self._crypto.hash_password(new_password)
        update = {
            "salt": salt,
            "password": hashed_pass,
            "password_modified": timestamp
        }
        self.options_collection.update({"option_type": "user", "username": current_username}, {"$set": update})

    def get_site_name(self):
        return self.options_collection.find_one({"option_type": "site_name"})

    def _add_site_name(self, site_name):
        timestamp = datetime.now()
        new_item = {
            "option_type": "site_name",
            "site_name": site_name,
            "date_created": timestamp,
            "date_modified": timestamp
        }
        self.options_collection.insert(new_item)

    def modify_site_name(self, site_name):
        timestamp = datetime.now()
        self.options_collection.update({"option_type": "site_name"}, {"$set": {"site_name": site_name, "date_modified": timestamp}})

    def get_def_ppp(self):
        return self.options_collection.find_one({"option_type": "def_ppp"})

    def _add_def_ppp(self, def_ppp):
        timestamp = datetime.now()
        new_item = {
            "option_type": "def_ppp",
            "def_ppp": def_ppp,
            "date_created": timestamp,
            "date_modified": timestamp
        }
        self.options_collection.insert(new_item)

    def modify_def_ppp(self, def_ppp):
        timestamp = datetime.now()
        self.options_collection.update({"option_type": "def_ppp"}, {"$set": {"def_ppp": def_ppp, "date_modified": timestamp}})

    #### RANKING ####

    # Mane
    def new_mane_rank(self):
        new_rank = {
            'rank_type': 'mane',
            'next_rank': 0
        }
        self.ranks_collection.insert(new_rank)

    def get_next_mane_rank(self):
        rank = self.ranks_collection.find_one({'rank_type': 'mane'})
        if not rank:
            self.new_mane_rank()
            return self.get_next_mane_rank()
        return rank.get('next_rank', 0)

    def increment_mane_rank(self, incr_value=1):
        self.ranks_collection.update({'rank_type': 'mane'}, {'$inc': {'next_rank': incr_value}})

    # Tail
    def new_tail_rank(self, mane):
        new_rank = {
            'rank_type': 'tail',
            'mane_name': mane.lower(),
            'next_rank': 0
        }
        self.ranks_collection.insert(new_rank)

    def get_next_tail_rank(self, mane):
        rank = self.ranks_collection.find_one({'rank_type': 'tail', 'mane_name': mane.lower()})
        if not rank:
            self.new_tail_rank(mane)
            return self.get_next_tail_rank(mane)
        return rank.get('next_rank', 0)

    def increment_tail_rank(self, mane, incr_value=1):
        self.ranks_collection.update({'rank_type': 'tail', 'mane_name': mane.lower()}, {'$inc': {'next_rank': incr_value}})

    def remove_tail_rank(self, mane):
        self.ranks_collection.remove({'rank_type': 'tail', 'mane_name': mane.lower()})

    # Post
    def new_post_rank(self, route_id):
        new_rank = {
            'rank_type': 'post',
            'route_id': route_id,
            'next_rank': 0
        }
        self.ranks_collection.insert(new_rank)

    def get_next_post_rank(self, route_id):
        rank = self.ranks_collection.find_one({'rank_type': 'post', 'route_id': route_id})
        if not rank:
            self.new_post_rank(route_id)
            return self.get_next_post_rank(route_id)
        return rank.get('next_rank', 0)

    def increment_post_rank(self, route_id, incr_value=1):
        self.ranks_collection.update({'rank_type': 'post', 'route_id': route_id}, {'$inc': {'next_rank': incr_value}})

    #### ROUTING ####
    def _insert_mane(self, mane_name, rank, title, desc):
        mane_name = unicode(mane_name)
        lowered_mane = mane_name.lower().replace(" ", "_")
        new_mane = {
            'mane_name': lowered_mane,
            'display': mane_name,
            'route_type': u'mane',
            'route_name': u'/{0}'.format(lowered_mane),
            'rank': rank,
            'title': unicode(title) if title else title,
            'desc': unicode(desc) if desc else desc
        }
        self.routes_collection.insert(new_mane)

    def _insert_tail(self, mane_name, tail_name, rank, title, desc):
        mane_name = unicode(mane_name).lower().replace(" ", "_")
        tail_name = unicode(tail_name)
        lowered_tail = tail_name.lower().replace(" ", "_")

        new_tail = {
            'mane_name': mane_name,
            'tail_name': lowered_tail,
            'display': tail_name,
            'route_type': u'tail',
            'route_name': u'/{0}/{1}'.format(mane_name, lowered_tail),
            'rank': rank,
            'title': unicode(title) if title else title,
            'desc': unicode(desc) if desc else desc
        }
        self.routes_collection.insert(new_tail)

    def add_new_mane(self, mane_name, rank, title=None, desc=None):
        rank = int(rank)

        self.routes_collection.update({'route_type': 'mane', 'rank': {'$gte': rank}},
                                    {'$inc': {'rank': 1}}, multi=True)

        self._insert_mane(mane_name, rank, title, desc)

    def add_new_tail(self, mane_name, tail_name, rank, title=None, desc=None):
        rank = int(rank)

        self.routes_collection.update({'route_type': 'tail', 'mane_name': mane_name, 'rank': {'$gte': rank}},
                                    {'$inc': {'rank': 1}}, multi=True)

        self._insert_tail(mane_name, tail_name, rank, title, desc)

    def remove_mane(self, mane_name):
        mane = self.get_mane(mane_name)
        self.routes_collection.remove({'mane_name': mane['mane_name']}, multi=True)

        self.routes_collection.update({'route_type': 'mane', 'rank': {'$gt': mane['rank']}},
                                    {'$inc': {'rank': -1}}, multi=True)

    def remove_tail(self, mane_name, tail_name):

        tail = self.get_tail(mane_name, tail_name)
        self.routes_collection.remove({'tail_name': tail['tail_name']})

        self.routes_collection.update({'route_type': 'tail', 'mane_name': tail['mane_name'], 'rank': {'$gt': tail['rank']}},
                                    {'$inc': {'rank': -1}}, multi=True)

    def get_manelinks(self):
        return self.routes_collection.find({'route_type': 'mane'}).sort('rank', 1)

    def get_taillinks(self, mane):
        return self.routes_collection.find({'route_type': 'tail', 'mane_name': mane.lower()}).sort('rank', 1)

    def get_links_for_mane(self, mane):
        manes = list(self.get_manelinks())
        tails = list(self.get_taillinks(mane))
        return manes, tails

    def get_mane_mane(self):
        mm = self.routes_collection.find({'route_type': 'mane'}).sort('rank', 1).limit(1)
        for mane in mm:
            return mane
        return None

    def get_mane(self, mane):
        return self.routes_collection.find_one({'route_type': 'mane', 'route_name': '/{0}'.format(mane.lower())})

    def get_tail(self, mane, tail):
        return self.routes_collection.find_one({'route_type': 'tail', 'route_name': '/{0}/{1}'.format(mane.lower(), tail.lower())})
