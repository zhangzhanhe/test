#!/usr/local/bin/python3
from urllib.request import urlopen
from urllib.request import Request
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import random
#爬虫间隔秒数
sleepTimerMin = 5;
sleepTimerMax = 10;
#请求数据
def getData(pageIndex):
	url='http://www2.tjfdc.gov.cn/pages/fcsdjsearch.aspx'
	header={
	   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
	}
	searchData={
		'__EVENTTARGET':'ctl00$PlaceHolderMain$g_db611ad9_e827_43dc_8a75_ad5743ca9dd1',
		'__EVENTARGUMENT':"dvt_firstrow={"+str(pageIndex)+"};dvt_startposition={}"
	}
	postdata=urllib.parse.urlencode(searchData).encode('utf8') #进行编码
	request=Request(url,postdata)
	reponse=urlopen(request).read()
	handleData(pageIndex,reponse);

#处理数据
def handleData(pageIndex,pageData):
	bsObj = BeautifulSoup(pageData,"html.parser")
	listObj = bsObj.find(id="WebPartWPQ2").findAll('tr');
	if(len(listObj) > 0):
		insertList = [];
		for item in listObj:
			itemText = item.findAll('td');
			#判断
			if(len(itemText) == 5):
				insertList.append({
					'id' : itemText[0].get_text(),
					'type' : itemText[1].get_text(),
					'company' : itemText[2].get_text(),
					'area' : itemText[3].get_text(),
					'address' : itemText[4].get_text(),
				})
		insertMongo(pageIndex,insertList);

#数据入库
def insertMongo(pageIndex,insertList):
	client = MongoClient("mongodb://localhost:27017/")
	db = client.tjHourse
	db.posts.insert(insertList)
	client.close();
	#一轮完成并给予提示
	print(pageIndex,':end');
	#沉睡后再跑一波
	delayTimer = random.randint(sleepTimerMin,sleepTimerMax)
	time.sleep(delayTimer)
	pageIndex = pageIndex + 20;
	getData(pageIndex);

#原始数据
pageIndex = 1;
getData(pageIndex);

