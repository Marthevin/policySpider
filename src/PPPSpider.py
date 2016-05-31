import urllib,urllib2
from bs4 import BeautifulSoup
import re

URL = "http://www.ndrc.gov.cn/fgwSearch/searchResult.jsp"
HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie':'JSESSIONID=37c8d8dd49d192d1ef879a566e23; gwdshare_firstime=1464105250075; _gscu_1828708336=64105250wfs11011; _gscs_1828708336=641052502b48yr11|pv:2; _gscbrs_1828708336=1; _gscu_1135328940=641052280tp6h312; _gscs_1135328940=64105228nghtwr12|pv:4;_gscbrs_1135328940=1',
'Host':'www.ndrc.gov.cn',
'Connection':'keep-alive',
'Origin':'http://www.ndrc.gov.cn',
'Referer':'http://www.ndrc.gov.cn/advSearch/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}
POST_DICT = {
'type':1,
'searchColumn':'',
'searchword':'PPP',
'wordFlag':'true',
'preSWord':'PPP',
'sword':'PPP',
'page':2,
'order':'-RELEVANCE',
'from':'',
'to':'',
'pageSize':20,
'extension':'',
'secondsearch2':''
}

POST_DATA = urllib.urlencode(POST_DICT)

request = urllib2.Request(URL,POST_DATA,HEADERS)
response = urllib2.urlopen(request)

bsoup = BeautifulSoup(response.read(),'lxml')
print bsoup.prettify()

#rec_list = bsoup.find_all(href=re.compile('^http://www.ndrc.gov.cn/.*[0-9]{5,8}\.html'))
#for rec in rec_list:
#    print rec['href']











