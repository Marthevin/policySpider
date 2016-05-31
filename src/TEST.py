import threading 
alist = [i for i in range(1000)]
class MyThread(threading.Thread):
    def __init__(self,name,i):
        global alist
        threading.Thread.__init__(self)
        self.l_list = alist[i-300:i]
        self.t_name = name
    
    def run(self):
        res = 0
        for x in self.l_list:
            res += x
        print self.t_name, res

def test():
    thread1 = MyThread('A',300)
    thread2 = MyThread('B',600)
    thread3 = MyThread('C',900)
    
    thread1.start()
    thread2.start()
    thread3.start()

if __name__ =='__main__':
    test()