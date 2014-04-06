import glob
import sys
import os
from osgeo import gdal
try:
    from utils import log, config, filesystem, ftp
except Exception, e:
    sys.path.append('../')
    from utils import log, config, filesystem, ftp


class gdal():

    def __init__(self, target_dir):
        """
        Initiate the logger for the class
        @param target_dir: Directory where to store the results
        """
        self.l = log.Logger()
        self.c = config.Config('MODIS')
        self.target_dir = target_dir
        self.ftp = ftp.FTPFENIX(self.c.get('ftp'), self.c.get('ftp_dir'))

    def list_subdatasets(self, filename):
        """
        List the sub-datasets of a layer
        @param filename: Name of the layer to read
        @return: List of available sub-datasets for the given layer
        """
        gtif = gdal.Open(self.target_dir + '/' + filename)
        list = []
        sds = gtif.GetSubDatasets()
        for tmp in sds:
            list.append(tmp[0])
        return list

    def extract_band(self, band):
        """
        Extract a given band from a layer
        @param band: Number of the band to extract, starting from 0
        @return: Full path of the required band
        """
        self.l.info('extract band ' + self.target_dir)
        files = []
        out = []
        for fname in glob.glob(self.target_dir + '/*.hdf'):
            files.append(fname)
        for file in files:
            gtif = gdal.Open(file)
            sds = gtif.GetSubDatasets()
            try:
                out.append(sds[int(band) - 1][0])
            except Exception, e:
                self.l.error('Exception for file "' + file + '"\n' + e)
        return out

    def modisDownloadExtractDelete(self, product, year, day, layer):
        filesystem.MODIS().createStructure(product, year, day)
        dir = self.c.getProperty('ftp_dir') + '/' + product + '/' + year + '/' + day + '/'
        targetDir = self.c.getProperty('targetDir') + '/' + product + '/' + year + '/' + day
        file = layer
        local_file = os.path.join(targetDir, file)
        if not os.path.exists(local_file):
            try:
                self.l.info('Downloading layer "' + layer + '"')
                if not os.path.exists(local_file):
                    self.l.info('Downloading: ' + local_file)
                    self.ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
                else:
                    self.l.info('Layer "' + layer + '" already exists. Skip.')
                self.ftp.quit()
                self.l.info('Download: done.')
            except Exception, e:
                self.l.error('Error while downloading layer: ' + layer)
                self.ftp.quit()
        gtif = gdal.Open(local_file)
        band = self.fixBandName(gtif.GetSubDatasets()[1][0])
        cmd = 'gdal_translate -q ' + band + ' ' + targetDir + '/' + layer.replace('.hdf', '.tif')
        try:
            os.system(cmd)
            self.l.info('GDAL Translate: done. [' + layer + ']')
        except Exception, e:
            self.l.error('Error during GDAL Translate: ' + e)