from threading import Thread
from ftplib import FTP
from utils import config
import os


class LayerDownloadThread(Thread):

    layer_name = None
    source_name = None
    total_size = 0
    download_size = 0

    def __init__(self, source_name, product, year, day, layer_name):

        Thread.__init__(self)

        self.source_name = source_name
        self.layer_name = layer_name
        self.product = product
        self.year = year
        self.day = day
        self.config = config.Config(self.source_name)

        ftp = FTP(self.config.get('ftp'))
        ftp.login()
        ftp.cwd(self.config.get('ftp_dir') + self.product + '/' + self.year + '/' + self.day + '/')
        ftp.sendcmd('TYPE i')
        self.total_size = ftp.size(self.layer_name)
        ftp.quit()

    def run(self):

        ftp = FTP(self.config.get('ftp'))
        ftp.login()
        ftp.cwd(self.config.get('ftp_dir') + self.product + '/' + self.year + '/' + self.day + '/')
        file = self.layer_name
        local_file = os.path.join(self.config.get('targetDir'), file)

        if not os.path.isfile(local_file):
            try:
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
        else:
            self.download_size = self.total_size

        ftp.quit()

    def percent_done(self):
        return float(self.download_size) / float(self.total_size) * 100