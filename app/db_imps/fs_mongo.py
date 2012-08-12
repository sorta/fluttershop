from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from bson.errors import InvalidId


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

    def get_post(self, post_id):
        post_id = self._qualify_oid(post_id)
        return self.posts_collection.find_one({'_id': post_id})

    def get_posts_for_tab(self, tab_id, post_limit=10):
        tab_id = self._qualify_oid(tab_id)
        return self.posts_collection.find({'parent': tab_id}).sort('rank', -1).limit(post_limit)

    def insert_new_post(self, tab_id, alignment, width, title, rank, show_title, show_date, post_content):
        post_col = self.posts_collection
        tab_id = self._qualify_oid(tab_id)
        rank = int(rank)

        timestamp = datetime.now()
        new_post = {
            "parent": tab_id,
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

        new_id = post_col.insert(new_post)
        self.update_post_ranks(tab_id, rank, ignore_id=new_id)

    def update_post(self, post_id, tab_id, alignment, width, title, rank, show_title, show_date, post_content):
        post_col = self.posts_collection
        tab_id = self._qualify_oid(tab_id)
        post_id = self._qualify_oid(post_id)
        rank = int(rank)

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
        self.update_post_ranks(tab_id, rank, ignore_id=post_id)

        zero_post = post_col.find_one({'parent': tab_id, 'rank': 0})
        if not zero_post:
            self.update_post_ranks(tab_id, 1, increment=-1)

    def remove_post(self, post_id):
        post_id = self._qualify_oid(post_id)
        post = self.get_post(post_id)
        if post:
            self.posts_collection.remove({'_id': post['_id']})
            self.update_post_ranks(post.get('parent', None), post['rank'], increment=-1)

    def remove_posts_for_tab(self, parent_id):
        parent_id = self._qualify_oid(parent_id)
        self.posts_collection.remove({'parent': parent_id})

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

    def get_def_ppp_num(self):
        def_ppp = self.get_def_ppp()
        if not def_ppp:
            return 12
        else:
            return def_ppp['def_ppp']

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

    def get_next_tab_rank(self, parent_id):
        parent_id = self._qualify_oid(parent_id)
        return self.routes_collection.find({'parent': parent_id}).count()

    def update_tab_ranks(self, parent_id, rank, ignore_id=None, increment=1):
        parent_id = self._qualify_oid(parent_id)
        ignore_id = self._qualify_oid(ignore_id)
        rank = int(rank)
        self.routes_collection.update({'parent': parent_id, 'rank': {'$gte': rank}, '_id': {'$ne': ignore_id}},
                                    {'$inc': {'rank': increment}}, multi=True)

    # Post

    def get_next_post_rank(self, parent_id):
        parent_id = self._qualify_oid(parent_id)
        return self.posts_collection.find({'parent': parent_id}).count()

    def update_post_ranks(self, parent_id, rank, ignore_id=None, increment=1):
        parent_id = self._qualify_oid(parent_id)
        ignore_id = self._qualify_oid(ignore_id)
        rank = int(rank)
        self.posts_collection.update({'parent': parent_id, 'rank': {'$gte': rank}, '_id': {'$ne': ignore_id}},
                                    {'$inc': {'rank': increment}}, multi=True)

    #### ROUTING ####
    def _qualify_oid(self, oid):
        if oid == None:
            return None

        try:
            val = ObjectId(oid)
        except InvalidId:
            val = None

        return val

    def _qualify_parent(self, parent_id):
        parent = self.get_tab(parent_id)

        if not parent:
            parent = {
                'path': '',
                '_id': None
            }

        return parent

    def _build_tab_data(self, tab_name, rank, title, desc, parent_id, nav_display, ppp):
        rank = int(rank)

        tab_name = tab_name
        clean_name = self._base_util.clean_name(tab_name)

        parent = self._qualify_parent(parent_id)
        path = u"{0}/{1}".format(parent.get('path', ''), clean_name)
        tab = {
            'name': clean_name,
            'display': tab_name,
            'path': path,
            'rank': rank,
            'title': unicode(title) if title else title,
            'desc': unicode(desc) if desc else desc,
            'parent': parent.get('_id', None),
            'nav_display': nav_display,
            'ppp': ppp
        }
        return tab

    def _insert_tab(self, tab_name, rank, title, desc, parent_id, nav_display, ppp):
        new_tab = self._build_tab_data(tab_name, rank, title, desc, parent_id, nav_display, ppp)
        return self.routes_collection.insert(new_tab)

    def add_new_tab(self, tab_name, rank, title=None, desc=None, parent_id=None, nav_display=True, ppp=12):
        parent_id = self._qualify_oid(parent_id)
        rank = int(rank)
        ppp = int(ppp)

        new_id = self._insert_tab(tab_name, rank, title, desc, parent_id, nav_display, ppp)
        if nav_display:
            self.update_tab_ranks(parent_id, rank, ignore_id=new_id)
        return new_id

    def edit_tab(self, tab_id, tab_name, rank, title=None, desc=None, parent_id=None, nav_display=True, ppp=12):
        parent_id = self._qualify_oid(parent_id)
        tab_id = self._qualify_oid(tab_id)
        rank = int(rank)
        ppp = int(ppp)

        updates = self._build_tab_data(tab_name, rank, title, desc, parent_id, nav_display, ppp)
        self.routes_collection.update({'_id': tab_id}, {'$set': updates})

        if nav_display:
            self.update_tab_ranks(parent_id, rank, ignore_id=tab_id)

        zero_route = self.routes_collection.find_one({'parent': parent_id, 'rank': 0})
        if not zero_route:
            self.update_tab_ranks(parent_id, 1, increment=-1)

    def remove_tab(self, tab_id):
        tab_id = self._qualify_oid(tab_id)
        tab = self.get_tab(tab_id)
        self.routes_collection.remove({'_id': tab['_id']})

        if tab['nav_display']:
            self.update_tab_ranks(tab.get('parent', None), tab['rank'], increment=-1)

    def get_tabs_by_parent(self, parent_id):
        parent_id = self._qualify_oid(parent_id)
        return list(self.routes_collection.find({'parent': parent_id}).sort('rank', 1))

    def get_tab_links(self, tab_id, parent_id, get_tail=True):
        links = []
        if parent_id:
            parent = self.get_tab(parent_id)
            links.extend(self.get_tab_links(parent['_id'], parent['parent'], False))

        links.append(self.get_tabs_by_parent(parent_id))
        if get_tail:
            links.append(self.get_tabs_by_parent(tab_id))

        return links

    def get_mane_tab(self):
        mm = self.routes_collection.find({'parent': None}).sort('rank', 1).limit(1)
        for mane in mm:
            return mane
        return None

    def get_tab(self, tab_id):
        tab_id = self._qualify_oid(tab_id)
        return self.routes_collection.find_one({'_id': tab_id})

    def get_tab_by_name(self, route_name):
        path = self._base_util.pathify_name(route_name, True)
        return self.routes_collection.find_one({'path': path})

    def get_path_by_tab(self, tab_id):
        tab_id = self._qualify_oid(tab_id)
        return self.routes_collection.find_one({'_id': tab_id}, fields=['path'])
