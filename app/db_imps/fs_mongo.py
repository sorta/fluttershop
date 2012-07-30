from datetime import datetime
import pymongo
from bson.objectid import ObjectId


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
    def routes_collection(self):
        return self._mdb.routes

    #### CONTENT ####

    def get_posts_for_route_by_name(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': unicode(route_id).lower()}).sort('rank', -1).limit(post_limit)

    def get_posts_for_route(self, route_id, post_limit=10):
        post_col = self.posts_collection
        return post_col.find({'route_id': ObjectId(route_id)}).sort('rank', -1).limit(post_limit)

    def insert_new_post(self, route, mane, alignment, width, title, rank, show_title, show_date, post_content, tail=None):
        post_col = self.posts_collection
        rank = int(rank)
        post_col.update({'route_id': route, 'rank': {'$gte': rank}}, {'$inc': {'rank': 1}}, multi=True)

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
            "rank": rank
        }

        if tail:
            new_post["tail_id"] = tail

        return post_col.insert(new_post)

    def update_post(self, post_id, route, alignment, width, title, rank, show_title, show_date, post_content):
        post_col = self.posts_collection
        rank = int(rank)
        post_col.update({'route_id': route, 'rank': {'$gte': rank}}, {'$inc': {'rank': 1}}, multi=True)

        post_id = ObjectId(post_id)

        timestamp = datetime.now()
        updates = {
            "post_content": post_content,
            "alignment": alignment,
            "width": width,
            "title": title,
            "show_title": show_title,
            "show_date": show_date,
            "date_modified": timestamp,
            "rank": rank
        }

        post_col.update({'_id': post_id}, {'$set': updates})

        zero_post = post_col.find({'route_id': route, 'rank': 0})
        if not zero_post.count():
            post_col.update({'rank': {'$gt': 0}}, {'$inc': {'rank': -1}}, multi=True)

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

    # Tab

    def get_next_tab_rank(self, parent):
        if parent:
            parent = ObjectId(parent)
        return self.routes_collection.find({'parent': parent}).count()

    def update_tab_ranks(self, parent, rank):
        self.routes_collection.update({'parent': parent, 'rank': {'$gte': rank}},
                                    {'$inc': {'rank': 1}}, multi=True)

    #### ROUTING ####
    def _build_tab_data(self, tab_name, rank, title, desc, parent, nav_display):
        rank = int(rank)
        tab_name = unicode(tab_name)
        clean_name = self._base_util.clean_name(tab_name)
        path = self._base_util.pathify_name(clean_name, True)
        tab = {
            'name': clean_name,
            'display': tab_name,
            'path': path,
            'rank': rank,
            'title': unicode(title) if title else title,
            'desc': unicode(desc) if desc else desc,
            'parent': ObjectId(parent) if parent else parent,
            'nav_display': nav_display
        }
        return tab

    def _insert_tab(self, tab_name, rank, title, desc, parent, nav_display):
        new_tab = self._build_tab_data(tab_name, rank, title, desc, parent, nav_display)
        self.routes_collection.insert(new_tab)

    def add_new_tab(self, tab_name, rank, title=None, desc=None, parent=None, nav_display=True):
        if nav_display:
            self.update_tab_ranks(parent, rank)
        self._insert_tab(tab_name, rank, title, desc, parent, nav_display)

    def edit_tab(self, tab_id, tab_name, rank, title=None, desc=None, parent=None, nav_display=True):
        if nav_display:
            self.update_tab_ranks(parent, rank)

        updates = self._build_tab_data(tab_name, rank, title, desc, parent, nav_display)
        self.routes_collection.update({'_id': tab_id}, {'$set': updates})

        zero_route = self.routes_collection.find_one({'route_type': 'tab', 'rank': 0})
        if not zero_route:
            self.routes_collection.update({'rank': {'$gt': 0}}, {'$inc': {'rank': -1}}, multi=True)

    def remove_tab(self, tab_id):
        tab = self.get_tab(tab_id)
        self.routes_collection.remove({'_id': tab['_id']})

        if tab['nav_display']:
            self.update_tab_ranks(tab['parent'], tab['rank'])

        for route in self.routes_collection.find({'parent': tab['_id']}):
            self.remove_tab(route['_id'])

    def get_tab_links(self):
        return list(self.routes_collection.find({'route_type': 'tab'}).sort('rank', 1))

    def get_mane_route(self):
        mm = self.routes_collection.find({'route_type': 'mane'}).sort('rank', 1).limit(1)
        for mane in mm:
            return mane
        return None

    def get_tab(self, route_id):
        return self.routes_collection.find_one({'_id': ObjectId(route_id)})

    def get_tab_by_name(self, route_name):
        path = self._base_util.pathify_name(route_name, True)
        return self.routes_collection.find_one({'path': path})
