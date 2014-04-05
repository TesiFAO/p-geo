import os
import sys
from ftplib import FTP
try:
    from utils import logging
except Exception, e:
    sys.path.append('../')
    from utils import logging


class FTP():

    def __init__(self, ftp, dir):
        """
        Initiate the logger for the class
        @param ftp: FTP address
        @param dir: Directory where to move after the login
        """
        self.l - logging.Logger()
        self.ftp = FTP(ftp)
        self.ftp.login()
        self.ftp.cwd(dir)

    def list_dir(self):
        """
        List the contents of a remote directory
        @return: Array containing all the file names
        """
        l = self.ftp.nlst()
        self.ftp.quit()
        return l

    def download(self, target_dir, filename):
        """
        Download a file from a FTP to a local directory
        @param target_dir: Local directory to store the remote file
        @param filename: Name of the remote file
        @return: A message to describe the status of the operation
        """
        file = filename
        local_file = os.path.join(target_dir, file)
        try:
            self.ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
            self.ftp.quit()
            return filename + ' successfully downloaded'
        except Exception, e:
            self.ftp.quit()
            return 'Error while downloading layer: ' + filename

    def download_list(self, target_dir, files):
        """
        Download a list of files from a FTP to a local directory
        @param target_dir: Local directory to store the remote file
        @param files: List of all the files to be downloaded
        @return: A message to describe the status of the operation
        """
        out = []
        for filename in files:
            self.l.info('Downloading: ' + filename)
            file = filename
            local_file = os.path.join(target_dir, file)
            if not os.path.exists(local_file):
                try:
                    self.ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
                    out.append(filename)
                except Exception, e:
                    pass
        self.ftp.quit()
        return out