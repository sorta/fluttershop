from hashlib import sha512
from datetime import datetime
import pymongo


class FShopMongoDB():

    def __init__(self, db_address, db_port=27017):
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
        return post_col.find({'route_id': unicode(route_id).lower()}).sort('rank', -1).limit(post_limit)

    def insert_new_post(self, route, mane, post_type, alignment, width, title, next_rank, tail=None):
        post_col = self.posts_collection
        new_post = {
            "route_id": route,
            "mane_id": mane,
            "post_type": post_type,
            "alignment": alignment,
            "width": width,
            "title": title,
            "timestamp": datetime.now(),
            "rank": next_rank
        }

        if tail:
            new_post["tail_id"] = tail

        return post_col.insert(new_post)

    def insert_new_post_part(self, post_id, part_type, body, next_rank, alt_text=None, caption=None):
        part_col = self.parts_collection
        new_part = {
            "post_id": post_id,
            "part_type": part_type,
            "body": body,
            "rank": next_rank,
            "timestamp": datetime.now()
        }

        if alt_text:
            new_part["alt_text"] = alt_text
        if caption:
            new_part["caption"] = caption

        part_col.insert(new_part)

    #### OPTIONS ####
    def get_user(self, username, password):
        prepared_pass = unicode(sha512(u'KsdfKSDFGT435Jwef45TJ6' + unicode(password)).hexdigest())
        return self.options_collection.find_one({'username': username, 'password': prepared_pass})

    def user_exists(self, username):
        return self.options_collection.find_one({'username': username})

    #### RANKING ####

    # Mane
    def get_next_mane_rank(self):
        return self.ranks_collection.find_one({'rank_type': 'mane'}).get('next_rank', 9000)

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
        return rank.get('next_rank', 9000)

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

        self.increment_mane_rank()

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

        self.increment_tail_rank(mane_name)

    def add_new_mane(self, mane_name, rank, title=None, desc=None):
        routes_to_increment = []
        manes = self.get_manelinks()
        for mane in manes:
            mane_rank = mane.get('rank', 9000)
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
            tail_rank = tail.get('rank', 9000)
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
                self.increment_mane_rank(-1)
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
                self.increment_tail_rank(mane_name, -1)
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
        manes = self.get_manelinks()
        tails = self.get_taillinks(mane)
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
