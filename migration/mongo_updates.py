import pymongo

conn = pymongo.Connection('192.168.0.199')
db = conn['fluttershop']


def post_update():
    psts = db.postparts.find({}, ['body', 'post_id'])

    for pst in psts:
        db.posts.update({'_id': pst['post_id']}, {'$set': {'post_content': pst['body']}})

    db.postparts.drop()


def tab_update1():
    coll = db.routes
    rts = list(coll.find())

    for rt in rts:
        rt['path'] = rt['route_name']
        rt['nav_display'] = True
        if rt['route_type'] == 'tail':
            parent = coll.find_one({'route_name': '/{0}'.format(rt['mane_name'])})
            rt['parent'] = parent['_id']
            rt['name'] = rt['tail_name']
        else:
            rt['name'] = rt['mane_name']
            rt['parent'] = None
        coll.save(rt)

    coll.update({}, {'$unset': {'mane_name': 1, 'tail_name': 1, 'route_name': 1, 'route_type': 1}}, multi=True)

    coll = db.posts
    posts = list(coll.find())

    for post in posts:
        if post.get('route_id', '') == '/404':
            coll.remove(post)
        else:
            parent = db.routes.find_one({'path': post['route_id']})
            post['parent'] = parent['_id']
            coll.save(post)

    coll.update({}, {'$unset': {'mane_id': 1, 'tail_id': 1, 'route_id': 1}}, multi=True)


def kill_ranks():
    coll = db.ranks
    coll.drop()
