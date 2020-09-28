from multiprocessing import Queue

q = Queue()
q.put({})
q.get()

size = q.qsize()
print(size)
