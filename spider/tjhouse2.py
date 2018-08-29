#!/usr/local/bin/python3
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

datetime = time.strftime("%Y-%m-%d",time.localtime(time.time() - 24*60*60))
#请求数据
def getData():
	url='http://111.160.20.142/pages/xwzw.aspx'
	header={
	   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
	}
	request=Request(url)
	reponse=urlopen(request).read()
	handleData(reponse);

#处理数据
def handleData(pageData):
	bsObj = BeautifulSoup(pageData,"html.parser");
	listObj = bsObj.find(class_="jiaoyi").find(id="clfqk_ul_lb").findAll('li');
	if(len(listObj) > 0):
		contractList = [];
		for item in listObj:
			itemText = item.findAll('p');
			#判断
			if(len(itemText) == 2):
				contractList.append({
					'contractId' : itemText[0].get_text(),
					'houseAddress' : itemText[1].get_text()				
				})
		insertMongo(contractList);

#数据入库
def insertMongo(contractList):
	client = MongoClient("mongodb://localhost:27017/")
	db = client.tjHourseContract
	db.posts.insert({
		'recordData' : datetime,
		'contractList' : contractList
	})
	client.close();
	#一轮完成并给予提示
getData();

