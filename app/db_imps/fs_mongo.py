from datetime import datetime
import pymongo


class FShopMongoDB():

    def __init__(self, crypto, db_address, db_port=27017):
        self._connection = pymongo.Connection(db_address, db_port)
        self._mdb = self._connection.fluttershop
        self._crypto = crypto

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
        return post_col.find({'route_id': unicode(route_id).lower()}).sort('rank', -1).limit(post_limit)

    def insert_new_post(self, route, mane, post_type, alignment, width, title, next_rank, show_title, show_date, tail=None):
        post_col = self.posts_collection
        timestamp = datetime.now()
        new_post = {
            "route_id": route,
            "mane_id": mane,
            "post_type": post_type,
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

    def insert_new_post_part(self, post_id, part_type, body, next_rank, alt_text=None, caption=None):
        part_col = self.parts_collection
        timestamp = datetime.now()
        new_part = {
            "post_id": post_id,
            "part_type": part_type,
            "body": body,
            "rank": next_rank,
            "date_created": timestamp,
            "date_modified": timestamp,
        }

        if alt_text:
            new_part["alt_text"] = alt_text
        if caption:
            new_part["caption"] = caption

        part_col.insert(new_part)

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

    # Post Parts
    def new_post_part_rank(self, post_id):
        new_rank = {
            'rank_type': 'post_part',
            'post_id': post_id,
            'next_rank': 0
        }
        self.ranks_collection.insert(new_rank)

    def get_next_post_part_rank(self, post_id):
        rank = self.ranks_collection.find_one({'rank_type': 'post_part', 'post_id': post_id})
        if not rank:
            self.new_post_part_rank(post_id)
            return self.get_next_post_part_rank(post_id)
        return rank.get('next_rank', 0)

    def increment_post_part_rank(self, post_id, incr_value=1):
        self.ranks_collection.update({'rank_type': 'post_part', 'post_id': post_id}, {'$inc': {'next_rank': incr_value}})

    #### ROUTING ####
    def _insert_mane(self, mane_name, rank, title, desc):
        mane_name = unicode(mane_name)
        lowered_mane = mane_name.lower()
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

        new_tail_rank = {
            'rank_type': 'tail',
            'mane_name': lowered_mane,
            'next_rank': 0
        }
        self.ranks_collection.insert(new_tail_rank)

    def _insert_tail(self, mane_name, tail_name, rank, title, desc):
        mane_name = unicode(mane_name).lower()
        tail_name = unicode(tail_name)
        lowered_tail = tail_name.lower()

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
        routes_to_increment = []
        manes = self.get_manelinks()
        for mane in manes:
            mane_rank = mane.get('rank', 0)
            if  mane_rank < rank:
                continue
            if mane_rank == rank:
                self._insert_mane(mane_name, mane_rank, title, desc)
            routes_to_increment.append(mane['route_name'])

        if not routes_to_increment:
            self._insert_mane(mane_name, rank, title, desc)
        else:
            self.routes_collection.update({'route_name': {'$in': routes_to_increment}}, {'$inc': {'rank': 1}}, multi=True)

    def add_new_tail(self, mane_name, tail_name, rank, title=None, desc=None):
        routes_to_increment = []
        tails = self.get_taillinks(mane_name)
        for tail in tails:
            tail_rank = tail.get('rank', 0)
            if  tail_rank < rank:
                continue
            if tail_rank == rank:
                self._insert_tail(mane_name, tail_name, tail_rank, title, desc)
            routes_to_increment.append(tail['route_name'])

        if not routes_to_increment:
            self._insert_tail(mane_name, tail_name, rank, title, desc)
        else:
            self.routes_collection.update({'route_name': {'$in': routes_to_increment}}, {'$inc': {'rank': 1}}, multi=True)

    def remove_mane(self, mane_name):
        routes_to_decrement = []
        target_acquired = False
        manes = self.get_manelinks()
        for mane in manes:
            if mane_name == mane['mane_name']:
                target_acquired = True
                self.routes_collection.remove({'mane_name': mane['mane_name']}, multi=True)
                self.ranks_collection.remove({'rank_type': 'tail', 'mane_name': mane['mane_name']})
                continue
            if target_acquired:
                routes_to_decrement.append(mane['route_name'])

        if routes_to_decrement:
            self.routes_collection.update({'route_name': {'$in': routes_to_decrement}}, {'$inc': {'rank': -1}}, multi=True)

    def remove_tail(self, mane_name, tail_name):
        routes_to_decrement = []
        target_acquired = False
        tails = self.get_taillinks(mane_name)
        for tail in tails:
            if tail_name == tail['tail_name']:
                target_acquired = True
                self.routes_collection.remove({'tail_name': tail['tail_name']})
                continue
            if target_acquired:
                routes_to_decrement.append(tail['route_name'])

        if routes_to_decrement:
            self.routes_collection.update({'route_name': {'$in': routes_to_decrement}}, {'$inc': {'rank': -1}}, multi=True)

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
