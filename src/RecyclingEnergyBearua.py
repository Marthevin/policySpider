# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import re
import thread,threading
from pymysql import Connection
URL = "http://searchxh.news.cn/was5/web/search?channelid=229767&searchword=%E5%8F%AF%E5%86%8D%E7%94%9F%E8%83%BD%E6%BA%90&prepage=&page="

LOCK = thread.allocate_lock()

#mysql connection
HOST = 'localhost'
USER='root'
PASSWORD='admin'
DATABASE='policyDB'
PORT= 3306
CHARSET = 'utf8mb4'
connection = Connection(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=PORT,charset=CHARSET)
cursor = connection.cursor()

#page info
num_count = 2550
numlist = [i for i in range(1,2550/10+1)]
pagenum = 1
rec_num = 0
#print bsoup.prettify()



class MyThread(threading.Thread):
    def __init__(self,name,fromIndex,toIndex):
        global numlist,URL
        threading.Thread.__init__(self)
        self.url = URL
        self.tname = name
        self.llist = numlist[fromIndex:toIndex]
        
    def run(self):
        global URL,rec_num,cursor,connection
        for i in self.llist:
            self.url = URL+str(i)
            #print self.url
            LOCK.acquire()
            try:
                response = urllib.urlopen(self.url)
            except :
                response = urllib.urlopen(self.url)
            LOCK.release()
            bsoup = BeautifulSoup(response.read())
            a_list = bsoup.find_all(href=re.compile('^http://www\..*[0-9]{8,12}\.htm'))
            time_list = bsoup.find_all('span','bold')
            rec = ()
            for i in range(len(a_list)):
                ele_a = a_list[i]
                ele_span = time_list[i]
                url = ele_a['href']
                title = ele_a.string
                pub_time = ele_span.string
                LOCK.acquire()
                rec_num +=1
                rec = (rec_num,url,title,pub_time)
                LOCK.release()
                #print rec
                try:
                    LOCK.acquire()
                    sql = "insert into url_recycling_energy_bearua values(%s,%s,%s,%s)" 
                    cursor.execute(sql,rec)
                    connection.commit()
                    LOCK.release()
                finally:
                    print self.url,"SUCCESS!"
        #connection.close()   
        thread.exit_thread()

def test():
    thread1 = MyThread('A',0,30)
    thread2 = MyThread('B',30,60)
    thread3 = MyThread('D',60,90)
    thread4 = MyThread('E',90,120)
    thread5 = MyThread('F',120,150)
    thread6 = MyThread('G',150,180)
    thread7 = MyThread('H',180,210)
    thread8 = MyThread('I',210,240)
    thread9 = MyThread('J',240,255)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()

       
if __name__ == '__main__':
    test()   