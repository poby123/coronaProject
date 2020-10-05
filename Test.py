from multiprocessing import Process, Queue
import time

#Handler는 모든 작업을 동기적으로 하게된다.
def Handler(q):
    while(True):
        if(q.qsize()>0):
            item = q.get()
            if(item == 'costTime'):
                success = costTime()
                print(success)
            elif(item == 'end'):
                print('end is called')
                return

def costTime():
    time.sleep(4)
    print('cost time is called')
    return 'cost time finished'

if __name__ == '__main__':
    q = Queue()
    handler = Process(target=Handler, args=(q,), daemon=True)
    handler.start()
    q.put('costTime')
    time.sleep(2)
    q.put('end')

    handler.join()