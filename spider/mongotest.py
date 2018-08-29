from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client.runoob
posts = db.site
for post in posts.find():
    print(post)
