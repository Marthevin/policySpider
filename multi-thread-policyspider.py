# -*- coding: utf-8 -*-
import threading
import thread
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
from pymysql import Connection

#define the global variance
URL  = 'http://search.chinalaw.gov.cn/v4luceneResult/fgSearchAdvance2.jsp'
HEADERS = {'Cookie':'_gscu_1215261538=62595339exfohx10; _gscs_1215261538=62595339s5fmmy10|pv:1; _gscbrs_1215261538=1; gwyfzb=20111111; JSESSIONID=94CE584C0E38DDD5C3193E477C217480',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
           'Referer': 'http://search.chinalaw.gov.cn/v4luceneResult/fgSearchAdvance2.jsp',
           'Connection':'keep-alive'
           }
POST_DICT = {'pageid':'1',
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

LOCK = thread.allocate_lock()
REC_ID = 1
#mysql connection info
HOST = 'localhost'
USER='root'
PASSWORD='admin'
DATABASE='policyDB'
PORT= 3306
CHARSET = 'utf8mb4'
connection = Connection(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=PORT,charset=CHARSET)
cursor = connection.cursor()
#############################
PAGE_NUM = 20
#get record count
def get_rec_count():
    data = urllib.urlencode(POST_DICT)
    request = urllib2.Request(URL,data,HEADERS)
    response = urllib2.urlopen(request)
    bs = BeautifulSoup(response.read(),"lxml")
    rec_count = int(bs.b.string)
    return rec_count
    
#get rec count
rec_count = get_rec_count()
page_count =  rec_count/20 if rec_count%20==0 else rec_count/20+1
num_list = [i for i in range(1,page_count+1)]
#num_list = [i for i in range(1,3)]
    
class MyThread(threading.Thread):
    def __init__(self,name,i):
        global num_list,POST_DICT,URL,HEADERS
        threading.Thread.__init__(self)
        self.t_name = name
        self.post_dict = POST_DICT
        self.url = URL
        self.headers = HEADERS
        self.llist = num_list[i-50+1:i]
        
        
    def run(self):
        global REC_ID
        rec = ()
        for i in self.llist:
            self.post_dict['pageid'] = str(i)
            data = urllib.urlencode(self.post_dict)
            LOCK.acquire()
            try:
                request = urllib2.Request(self.url,data,self.headers)
                response = urllib2.urlopen(request)
            except:
                request = urllib2.Request(self.url,data,self.headers)
                response = urllib2.urlopen(request)
            
            LOCK.release()
            bsoup = BeautifulSoup(response.read())
            result_set = bsoup.find_all(href=re.compile('^http://fgk.chinalaw.gov.cn/'))
            for a in result_set:
                url = a['href']
                strings = a.strings
                name = ""
                for string in strings:
                    name+=string
                #print name.strip()
                rec = (REC_ID,url,name.strip())
                
                # insert into database
                try:
                    LOCK.acquire()
                    sql = "insert into URL values(%s,%s,%s)" 
                    cursor.execute(sql,rec)
                    connection.commit()
                    REC_ID+=1
                    LOCK.release()
                finally:
                    print REC_ID, "SUCCESS" 
        #connection.close()   
        thread.exit_thread()

def test():
    global rec_count
    thread1 = MyThread('A',1)
    thread2 = MyThread('B',50)
    thread3 = MyThread('C',100)
    thread4 = MyThread('D',150)
    thread5 = MyThread('E',200)
    thread6 = MyThread('F',page_count)
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()

if __name__ == '__main__':
    test()        
        
        
        
        
        
        
        
        
        
        
