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
product = 'MOD13A2'
year = '2014'
day = '001'

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
            raster.modisDownloadExtractDelete(product, year, '001', data)
            queueLock.release()
            l.info(threadName + ' processing ' + data)
        else:
            queueLock.release()
        time.sleep(1)

layers = ftp.listDir('ladsweb.nascom.nasa.gov', '/allData/5/' + product + '/' + year + '/' + day + '/')

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

# Read configuration file
bands = c.get('bands')
subfolders = c.get('subfolders')

# Iterate over bands
for band in bands:

    # Create global HDF
    l.info('Create global HDF for ' + band + ': START...')
    name = product + '.' + year + '.' + day + '.' + band + '.hdf'
    src = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['tmp'] + '/*.hdf'
    out = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['output'] + '/' + name
    if not os.path.exists(out):
        os.system('gdal_merge.py -n -3000 -a_nodata 0 ' + src + ' -o ' + out)
    else:
        l.info(out + ' already exists')
    l.info('Create global HDF for ' + band + ': DONE.')

    # Create 4326 projection
    l.info('Create 4326 TIF for ' + band + ': START...')
    src = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['output'] + '/' + name
    name = product + '.' + year + '.' + day + '.' + band + '.4326.tif'
    out = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['output'] + '/' + name
    if not os.path.exists(out):
        os.system("gdalwarp -srcnodata 0 -dstnodata nodata -multi -of GTiff -tr 0.00833333 -0.00833333  -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -co 'TILED=YES' -t_srs EPSG:4326 " + src + " " + out)
    else:
        l.info(out + ' already exists')
    l.info('Create 4326 TIF for ' + band + ': DONE.')

    # Create overviews
    l.info('Create overviews for ' + band + ': START...')
    cp = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['output'] + '/' + name
    name = product + '.' + year + '.' + day + '.' + band + '.4326.OVERVIEWS.tif'
    out = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + band + '/' + subfolders['output'] + '/' + name
    if not os.path.exists(out):
        os.system('cp ' + cp + ' ' + out)
        os.system('gdaladdo -r average ' + out + ' 2 4 8 16')
    else:
        l.info(out + ' already exists')
    l.info('Create overviews for ' + band + ': DONE.')