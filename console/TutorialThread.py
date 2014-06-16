from threading import Thread
from ftplib import FTP
from utils import config
import os

class TutorialThread(Thread):

    layerName = None
    sourceName = None
    totSize = 0
    dwldSize = 0

    def __init__(self, sourceName, layerName):

        Thread.__init__(self);

        self.sourceName = sourceName
        self.layerName = layerName
        self.config = config.Config(self.sourceName)

        ftp = FTP(self.config.get('ftp'))
        ftp.login()
        ftp.cwd('/allData/5/MOD13Q1/2014/001/')
        ftp.sendcmd('TYPE i')
        self.totSize = ftp.size(self.layerName)
        ftp.quit()

    def run(self):

        ftp = FTP(self.config.get('ftp'))
        ftp.login()
        ftp.cwd('/allData/5/MOD13Q1/2014/001/')
        file = self.layerName
        local_file = os.path.join(self.config.get('targetDir'), file)

        with open(local_file, 'w') as f:
            def callback(chunk):
                f.write(chunk)
                self.dwldSize += len(chunk)
            ftp.retrbinary('RETR %s' %file, callback)

        ftp.quit()

    def percent_done(self):
        return float(self.dwldSize) / float(self.totSize) * 100