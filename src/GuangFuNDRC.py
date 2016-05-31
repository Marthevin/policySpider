# -*- coding: utf-8 -*-

'''
光伏
OK NOT Running
'''
import urllib,urllib2
from bs4 import BeautifulSoup
import thread,threading
from pymysql import Connection
import time

URL = 'http://www.ndrc.gov.cn/fgwSearch/searchResult.jsp'

LOCK = thread.allocate_lock()
rec_count = 0

HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Connection':'keep-alive',
'Content-Type':'application/x-www-form-urlencoded',
'Cookie':'JSESSIONID=7616193446dee6e9936512dc273e; gwdshare_firstime=1464105250075; _gscu_1828708336=64105250wfs11011; _gscu_1135328940=641052280tp6h312; _gscs_1135328940=64438997myyolx12|pv:1; _gscbrs_1135328940=1',
'Host':'www.ndrc.gov.cn',
'Origin':'http://www.ndrc.gov.cn',
'Referer':'http://www.ndrc.gov.cn/fgwSearch/searchResult.jsp',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}

FORM_DATA = {
'type':'1',
'searchColumn':'',
'searchword':'光伏',                                     ######## 关键词 ##################
'wordFlag':'true',
'preSWord':'光伏',                                        ######## 关键词 ##################
'sword':'光伏',                                           ######## 关键词 ##################
'page':2,
'order':'-RELEVANCE',
'from':'',
'to':'',
'pageSize':20,
'extension':'',
'secondsearch2':''
}

#mysql connection
HOST = 'localhost'
USER='root'
PASSWORD='admin'
DATABASE='policyDB'
PORT= 3306
CHARSET = 'utf8mb4'
connection = Connection(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=PORT,charset=CHARSET)
cursor = connection.cursor()

rec_num = 2525                                                               #########################  need modification  ####################
rec_list = [i for i in range(1,rec_num/FORM_DATA['pageSize']+2)]              #################  127 pages ######################

#POST_DATA = urllib.urlencode(FORM_DATA)
#
#request = urllib2.Request(url=URL,data=POST_DATA,headers=HEADERS)
#response = urllib2.urlopen(request)

#bsoup = BeautifulSoup(response.read())
#print bsoup.prettify()

#resultset_a = bsoup.find_all('a','url')
#resultset_time = bsoup.find_all('font','dateShow')

#for i in range(len(resultset_a)):
#    ele_a = resultset_a[i]
#    ele_time = resultset_time[i]
#    print ele_a.string,ele_a['title'].replace('<font color=\'#f00000\'>','').replace('</font>',''),ele_time.string.replace('- (','').replace(')','')
    
class MyThread(threading.Thread):
    def __init__(self,name,fromIndex,toIndex):
        global rec_list,URL,HEADERS,POST_DATA
        threading.Thread.__init__(self)
        self.url = URL
        self.headers = HEADERS
        self.tname = name
        self.llist = rec_list[fromIndex:toIndex]
        
    def run(self):
        global rec_count,connection,LOCK,FORM_DATA
        for i in self.llist:
            FORM_DATA['page'] = i
            self.data = urllib.urlencode(FORM_DATA)
            #print self.url
            LOCK.acquire()
            try:
                request = urllib2.Request(url=self.url,data=self.data,headers=self.headers)
                response = urllib2.urlopen(request)
                time.sleep(0.2)
            except :
                request = urllib2.Request(url=self.url,data=self.data,headers=self.headers)
                response = urllib2.urlopen(request)
                time.sleep(0.5)
            LOCK.release()
            bsoup = BeautifulSoup(response.read(),'lxml')
            resultset_a = bsoup.find_all('a','url')
            resultset_time = bsoup.find_all('font','dateShow')
            rec = ()
            for j in range(len(resultset_a)):
                ele_a = resultset_a[j]
                ele_time = resultset_time[j]
                #print ele_a.string,ele_a['title'].replace('<font color=\'#f00000\'>','').replace('</font>',''),ele_time.string.replace('- (','').replace(')','')
                url = ele_a.string
                title = ele_a['title'].replace('<font color=\'#f00000\'>','').replace('</font>','')
                pubtime = ele_time.string.replace('- (','').replace(')','')
                LOCK.acquire()
                rec_count +=1
                rec = (rec_count,url,title,pubtime)
                LOCK.release()
                try:
                    LOCK.acquire()
                    sql = "insert into ndrc_guangfu values(%s,%s,%s,%s)"   ################# need modification of table ####################
                    cursor.execute(sql,rec)
                    connection.commit()
                    LOCK.release()
                finally:
                    print "page ",str(i)," SUCCESS!"
        #connection.close()   
        thread.exit_thread()
            

def test():
    thread1 = MyThread('A',0,10)
    thread2 = MyThread('B',10,20)
    thread3 = MyThread('D',20,30)
    thread4 = MyThread('E',30,40)
    thread5 = MyThread('F',40,50)
    thread6 = MyThread('G',50,60)
    thread7 = MyThread('H',60,70)
    thread8 = MyThread('I',70,80)
    thread9 = MyThread('J',80,90)
    thread10 = MyThread('K',90,100)
    thread11 = MyThread('L',100,110)
    thread12 = MyThread('M',110,120)
    thread13 = MyThread('N',120,127)
    #thread14 = MyThread('O',260,281)
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    thread12.start()
    thread13.start()
    #thread14.start()

       
if __name__ == '__main__':
    test()     