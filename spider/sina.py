import subprocess
from pymongo import MongoClient
import time
import json
#调用sina来获取数据
siteList=json.loads(subprocess.check_output(['phantomjs','sina.js']).decode('utf-8'))
#爬去数据的时间
datetime = time.strftime("%Y-%m-%d",time.localtime())

client = MongoClient("mongodb://localhost:27017/")
db = client.sinahw
searchList = list(db.posts.find({'innerDate':datetime}))
if(len(searchList) == 0):
	db.posts.insert({
		'innerDate' : datetime,
		'innerList' : siteList
	})
else:
	existData = searchList[0]['innerList'];
	print(len(existData))
	#先提取现有的关键词
	existKeyWord = [];
	for item in existData:
		existKeyWord.append(item['keyWord'])
	#根据现有关键词判断此次获取到的关键词是否插入
	for siteItem in siteList:
		if(siteItem['keyWord'] not in existKeyWord):
			existData.append(siteItem)
	#更新插入
	db.posts.update({'innerDate':datetime},{"$set":{'innerList':existData}})
client.close()
print('done:'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))