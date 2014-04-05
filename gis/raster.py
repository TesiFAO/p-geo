import glob
import sys
from osgeo import gdal
try:
    from utils import logging
except Exception, e:
    sys.path.append('../')
    from utils import logging


class gdal():

    def __init__(self, target_dir):
        """
        Initiate the logger for the class
        @param target_dir: Directory where to store the results
        """
        self.l = logging.Logger()
        self.target_dir = target_dir

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