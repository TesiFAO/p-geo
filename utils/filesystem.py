import os
import sys
try:
    from utils import logging, config
except Exception, e:
    sys.path.append('../')
    from utils import logging, config


class MODIS():

    def __init__(self):
        """
        Initiate the logger and the configuration
        """
        self.l - logging.Logger()
        self.c = config.Config('MODIS')

    def create_modis_structure(self, product, year, day):
        """
        Create the MODIS filesystem structure
        @param product: Name of the MODIS product
        @param year: Year, e.g. 2014
        @param day: Day, e.g. 001
        """
        if not os.path.exists(self.c.getProperty('targetDir') + '/' + product):
            os.makedirs(self.c.getProperty('targetDir') + '/' + product)
        if not os.path.exists(self.c.getProperty('targetDir') + '/' + product + '/' + year):
            os.makedirs(self.c.getProperty('targetDir') + '/' + product + '/' + year)
        if not os.path.exists(self.c.getProperty('targetDir') + '/' + product + '/' + year + '/' + day):
            os.makedirs(self.c.getProperty('targetDir') + '/' + product + '/' + year + '/' + day)

    def fix_band_name(self, n):
        """
        Remove spaces from MODIS bands name
        @param n: MODIS sub-dataset name
        @return: MODIS sub-dataset name without spaces
        """
        out = ''
        for c in n:
            if c == ' ':
                out += '\ '
            else:
                out += c
        return out