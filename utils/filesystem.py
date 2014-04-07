import os
import sys
try:
    from utils import log, config
except Exception, e:
    sys.path.append('../')
    from utils import log, config


l = log.Logger('filesystem')
c = config.Config('MODIS')

def create_modis_structure(product, year, day):
    """
    Create the MODIS filesystem structure
    @param product: Name of the MODIS product
    @param year: Year, e.g. 2014
    @param day: Day, e.g. 001
    """
    if not os.path.exists(c.get('targetDir') + '/' + product):
        os.makedirs(c.get('targetDir') + '/' + product)
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year)
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day)
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/EVI/'):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/EVI/')
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/EVI/original/'):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/EVI/original/')

def fix_band_name(name):
    """
    Remove spaces from MODIS bands name
    @param name: MODIS sub-dataset name
    @return: MODIS sub-dataset name without spaces
    """
    out = ''
    for c in name:
        if c == ' ':
            out += '\ '
        else:
            out += c
    return out