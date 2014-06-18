from threading import Thread
from threading import Lock
import Queue
from ftplib import FTP
from utils import config
from console import thread_manager_processes
from console import threads_map_key
import os
import uuid
import time

exitFlag = 0


class LayerDownloadThread(Thread):

    layer_name = None
    source_name = None
    total_size = 0
    download_size = 0

    def __init__(self, source_name, product, year, day, thread_name, q, key):

        Thread.__init__(self)

        self.source_name = source_name
        self.thread_name = thread_name
        self.product = product
        self.year = year
        self.day = day
        self.config = config.Config(self.source_name)
        self.q = q
        self.key = key

    def run(self):

        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                self.layer_name = self.q.get()
                queueLock.release()
                ftp = FTP(self.config.get('ftp'))
                ftp.login()
                ftp.cwd(self.config.get('ftp_dir') + self.product + '/' + self.year + '/' + self.day + '/')
                ftp.sendcmd('TYPE i')
                self.total_size = ftp.size(self.layer_name)
                file = self.layer_name
                local_file = os.path.join(self.config.get('targetDir'), file)
                if not os.path.isfile(local_file):
                    try:
                        print '>>> ' + os.stat(local_file).st_size + ' <<<'
                        fileSize = os.stat(local_file).st_size
                        if fileSize < self.total_size:
                            with open(local_file, 'w') as f:
                                def callback(chunk):
                                    f.write(chunk)
                                    self.download_size += len(chunk)
                                ftp.retrbinary('RETR %s' %file, callback)
                    except:
                        with open(local_file, 'w') as f:
                            def callback(chunk):
                                f.write(chunk)
                                self.download_size += len(chunk)
                            ftp.retrbinary('RETR %s' %file, callback)
                ftp.quit()
            else:
                queueLock.release()
            time.sleep(1)

    def percent_done(self):
        print str(self.download_size) + ' / ' + str(self.total_size)
        return float(self.download_size) / float(self.total_size) * 100


nameList = ["MOD13Q1.A2014001.h10v02.005.2014018100659.hdf", "MOD13Q1.A2014001.h10v03.005.2014018122614.hdf",
            "MOD13Q1.A2014001.h10v04.005.2014018095113.hdf", "MOD13Q1.A2014001.h10v05.005.2014018095025.hdf",
            "MOD13Q1.A2014001.h10v06.005.2014018090148.hdf", "MOD13Q1.A2014001.h10v07.005.2014018084024.hdf",
            "MOD13Q1.A2014001.h10v08.005.2014018090845.hdf", "MOD13Q1.A2014001.h10v09.005.2014018095633.hdf",
            "MOD13Q1.A2014001.h10v10.005.2014018083448.hdf", "MOD13Q1.A2014001.h10v11.005.2014018090632.hdf"]
threadList = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet', 'Kilo']
queueLock = Lock()
workQueue = Queue.Queue(len(nameList))
threads = []

for tName in threadList:
    key = uuid.uuid4()
    thread = LayerDownloadThread('MODIS', 'MOD13Q1', '2014', '001', tName, workQueue, key)
    thread.start()
    if not threads_map_key in thread_manager_processes:
        thread_manager_processes[threads_map_key] = {}
    thread_manager_processes[threads_map_key][key] = thread
    print 'MGR | ' + str(thread_manager_processes[threads_map_key])
    threads.append(thread)

queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

while not workQueue.empty():
    pass

exitFlag = 1

for t in threads:
    t.join()
print 'Exiting Main Thread - Do Some More Stuff...'