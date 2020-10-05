from multiprocessing import Process, Value

def foo(x):  
    for i in range(10000): 
         x.value += 1

def bar(x): 
    for i in range(10000): 
        x.value -= 1

if __name__ == '__main__':
    x = Value('d', 0)
    p1 = Process(target=foo, args=(x,))
    p2 = Process(target=bar, args=(x,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(x.value)
