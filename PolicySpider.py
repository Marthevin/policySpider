# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
from pymysql import Connection
import re
rec_id = 1
url = 'http://search.chinalaw.gov.cn/v4luceneResult/fgSearchAdvance2.jsp'

headers = {'Cookie':'_gscu_1215261538=62595339exfohx10; _gscs_1215261538=62595339s5fmmy10|pv:1; _gscbrs_1215261538=1; gwyfzb=20111111; JSESSIONID=94CE584C0E38DDD5C3193E477C217480',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
           'Referer': 'http://search.chinalaw.gov.cn/v4luceneResult/fgSearchAdvance2.jsp',
           'Connection':'keep-alive'
           }
           
post_dict = {'pageid':'1',
             'd_channel':'dffg',
             'fromwhere':'chinalaw_article',
             'key':'新能源',
             'title':'',
             'category':'',
             'sourceType':'',
             'area':'',
             'startTime':'',
             'endTime':'',
             'indexPathName':'indexPath2'
           }
           
HOST = 'localhost'
USER='root'
PASSWORD='admin'
DATABASE='policyDB'
PORT= 3306
CHARSET = 'utf8mb4'
connection = Connection(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=PORT,charset=CHARSET)
cursor = connection.cursor()

data = urllib.urlencode(post_dict)
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
bs = BeautifulSoup(response.read(),"lxml")
#print bs.prettify()

rec_count = int(bs.b.string)
rec_per_page = 20
page_count = rec_count/20 if rec_count%20==0 else rec_count/20+1
#print page_count

urls = []
names = []
for i in range(1,2):
    post_dict = {'pageid':str(i),
                'd_channel':'dffg',
                'fromwhere':'chinalaw_article',
                'key':'新能源',
                'title':'',
                'category':'',
                'sourceType':'',
                'area':'',
                'startTime':'',
                'endTime':'',
                'indexPathName':'indexPath2'
               }
    data = urllib.urlencode(post_dict)
    request = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(request)
    bs = BeautifulSoup(response.read())
    result_set = bs.find_all(href=re.compile('^http://fgk.chinalaw.gov.cn/'))
    for a in result_set:
        url = a['href']
        strings = a.strings
        name = ""
        for string in strings:
            name +=string
        rec = (rec_id,url,name.strip())
        try:
            sql = "insert into URL values(%s,%s,%s)"
            cursor.execute(sql,rec)
            connection.commit()
        finally:
            print "SUCCESS"

connection.close()
