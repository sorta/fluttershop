import pymongo

conn = pymongo.Connection('192.168.0.199')
db = conn['fluttershop']
psts = db.postparts.find({},['body', 'post_id'])

for pst in psts:
    db.posts.update({'_id': pst['post_id']}, {'$set': {'post_content': pst['body']}})

db.postparts.drop()
