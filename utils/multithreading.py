import Queue
import threading
import time
import sys
import os
from gis import raster
try:
    from utils import log, config, ftp
except Exception, e:
    sys.path.append('../')
    from utils import log, config, ftp

exitFlag = 0
c = config.Config('MODIS')
l = log.Logger()

class MODIS(threading.Thread):

    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        l.info('Starting ' + self.name)
        process_data(self.name, self.q)
        l.info('Exiting ' + self.name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            raster.modisDownloadExtractDelete('MOD13A2', '2014', '001', data)
            queueLock.release()
            l.info(threadName + ' processing ' + data)
        else:
            queueLock.release()
        time.sleep(1)

layers = ftp.listDir('ladsweb.nascom.nasa.gov', '/allData/5/MOD13A2/2014/001/')

threadList = []
for i in range(0, c.get('threads')):
    threadList.append('T' + str(i))

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
l.info('Exiting Main Thread')

l.info('Create global hdf: START...')
if not os.path.exists('/home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out.hdf'):
    os.system('gdal_merge.py -n -3000 -a_nodata 0 /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/tmp/*.hdf -o /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out.hdf')
l.info('Create global hdf: DONE.')

l.info('Create 4326 TIF: START...')
if not os.path.exists('/home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326.hdf'):
    os.system("gdalwarp -srcnodata 0 -dstnodata nodata -multi -of GTiff -tr 0.00833333 -0.00833333  -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -co 'TILED=YES' -t_srs EPSG:4326 /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out.hdf /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326.tif")
l.info('Create 4326 TIF: DONE.')

l.info('Create overviews: START...')
if not os.path.exists('/home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326_overviews.hdf'):
    os.system('cp /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326.tif /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326_overviews.tif')
    os.system('gdaladdo -r average /home/kalimaha/Desktop/MODIS/MOD13A2/2014/001/EVI/output/out_4326_overviews.tif 2 4 8 16')
l.info('Create overviews: DONE.')