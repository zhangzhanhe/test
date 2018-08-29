from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

sietList = []
bsObj = BeautifulSoup(urlopen("http://hao.360.cn/zhengfubumen.html"),"html.parser")
listObj = bsObj.findAll(class_="site-nav")
for item in listObj:
	typeTitle = item.find(class_="site-header").get_text()
	resultItem = {
		"typeTitle" : typeTitle,
		"typeList" : []
	}
	typeList = item.findAll("li")
	for inItem in typeList:
		itemObj = inItem.find('a')
		if itemObj:
			resultItem["typeList"].append({
				"url" : itemObj.attrs["href"],
				"name" : itemObj.get_text()
			})
	sietList.append(resultItem)

listWapper = {"list" : sietList}
with open('result.json','w',encoding='utf8') as f:
	f.write(json.dumps(listWapper,ensure_ascii=False))

print('done')