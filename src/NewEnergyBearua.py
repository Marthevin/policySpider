import urllib
from bs4 import BeautifulSoup
import re
import thread,threading
from pymysql import Connection
URL = "http://searchxh.news.cn/was5/web/search?channelid=229767&searchword=%E6%96%B0%E8%83%BD%E6%BA%90&prepage=&page="

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
num_count = 2888
numlist = [i for i in range(1,num_count/10+2)]
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
                    sql = "insert into url_new_energy_bearua values(%s,%s,%s,%s)" 
                    cursor.execute(sql,rec)
                    connection.commit()
                    LOCK.release()
                finally:
                    print self.url,"SUCCESS!"
        #connection.close()   
        thread.exit_thread()

def test():
    thread1 = MyThread('A',288,289)
    #thread1 = MyThread('A',0,20)
    #thread2 = MyThread('B',20,40)
    #thread3 = MyThread('D',40,60)
    #thread4 = MyThread('E',60,80)
    #thread5 = MyThread('F',80,100)
    #thread6 = MyThread('G',100,120)
    #thread7 = MyThread('H',120,140)
    #thread8 = MyThread('I',140,160)
    #thread9 = MyThread('J',160,180)
    #thread10 = MyThread('K',180,200)
    #thread11 = MyThread('L',200,220)
    #thread12 = MyThread('M',220,240)
    #thread13 = MyThread('N',240,260)
    #thread14 = MyThread('O',260,281)
    #
    #thread1.start()
    #thread2.start()
    #thread3.start()
    #thread4.start()
    #thread5.start()
    #thread6.start()
    #thread7.start()
    #thread8.start()
    #thread9.start()
    #thread10.start()
    #thread11.start()
    #thread12.start()
    #thread13.start()
    #thread14.start()
    thread1.start()
       
if __name__ == '__main__':
    test()   