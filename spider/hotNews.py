#!/usr/local/bin/python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time


datetime = time.strftime("%Y-%m-%d",time.localtime())
siteList = []

#爬取以及处理字段
bsResult = urlopen("http://top.baidu.com/buzz?b=1").read().decode('gbk','ignore')
bsObj = BeautifulSoup(bsResult,"html.parser")
listObj = bsObj.find(class_="list-table").findAll('tr')

for item in listObj:
	keyWordsItem = item.find('a',class_="list-title")
	if(keyWordsItem):
		siteList.append({
			'keyWord' : keyWordsItem.get_text(),
			'keyWordUrl' : keyWordsItem.attrs["href"],
			'keyWordIndex' : item.find('td',class_="last").find('span').get_text()
 		})



#入库
client = MongoClient("mongodb://localhost:27017/")
db = client.baiduhw
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