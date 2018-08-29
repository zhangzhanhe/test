from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import io
import gzip

def unzip(data):
    data = io.BytesIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data

header={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7,it;q=0.6,he;q=0.5,nl;q=0.4,ru;q=0.3',
   	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'locationddPro=%u5317%u4EAC%u5E02; pcsuv=1493434990998.ax.259285627; u4ad=491si571a; padex=491si571a; u=39pjgah; c=39oagly; channel=9472; pcLocate=%7B%22proCode%22%3A%22110000%22%2C%22pro%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22cityCode%22%3A%22110000%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22dataType%22%3A%22ipJson%22%2C%22expires%22%3A1533220830316%7D; pcautoLocate=%7B%22proId%22%3A6%2C%22cityId%22%3A2%2C%22url%22%3A%22http%3A%2F%2Fwww.pcauto.com.cn%2Fqcbj%2Fbj%2F%22%2C%22dataTypeAuto%22%3A%22region_ipArea%22%7D; __v2aab4922516ae9ec4fc92a7ba907b438=610e327851d3dc8d76e2f37b98d57ca8; pcuvdata=lastAccessTime=1531926025610|visits=6',
	'Host': 'price.pcauto.com.cn',
	'Upgrade-Insecure-Requests': 1,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
url='http://price.pcauto.com.cn/price/newpower/q-rl10000-n8.html'
request=Request(url=url,headers=header);
url_html=unzip(urlopen(request).read()).decode('gbk','ignore').encode('UTF-8');
url_content = BeautifulSoup(url_html,'html.parser')
car = url_content.find("div",{"id":"JlistTb"}).findAll(class_="j-list")
for i in (range(0,len(car))):
    print(car[i].findAll(class_="sname")[0].get_text())