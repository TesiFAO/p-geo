import Queue
import threading
import time
from gis import raster
from utils import ftp

exitFlag = 0

class MODIS(threading.Thread):

    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print 'Starting ' + self.name
        process_data(self.name, self.q)
        print 'Exiting ' + self.name

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            raster.modisDownloadExtractDelete('MOD13A2', '2014', '001', data)
            queueLock.release()
            print '%s processing %s' % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

layers = ftp.listDir('ladsweb.nascom.nasa.gov', '/allData/5/MOD13A2/2014/001/')

threadList = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
nameList = layers
queueLock = threading.Lock()
workQueue = Queue.Queue(len(layers))
threads = []
threadID = 1

# Create new threads
for tName in threadList:
    thread = MODIS(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"