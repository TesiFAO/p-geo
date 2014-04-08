import os
import sys
import uuid
try:
    from utils import log, config
except Exception, e:
    sys.path.append('../')
    from utils import log, config


l = log.Logger('filesystem')
c = config.Config('MODIS')
g = config.Config('general')

def create_modis_structure(product, year, day):
    """
    Create the MODIS filesystem structure
    @param product: Name of the MODIS product
    @param year: Year, e.g. 2014
    @param day: Day, e.g. 001
    """

    # Main structure
    if not os.path.exists(c.get('targetDir') + '/' + product):
        os.makedirs(c.get('targetDir') + '/' + product)
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year)
    if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day):
        os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day)

    #  Sub-folders for the bands
    bands = c.get('bands')
    subfolders = c.get('subfolders')
    for k in bands:
        if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + k + '/'):
            os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + k + '/')
        for s in subfolders:
            if not os.path.exists(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + k + '/' + s + '/'):
                os.makedirs(c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + k + '/' + s + '/')

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

def tmp_filename(prefix='', extension=''):
    # the utf-8 encoding it's used to create a new .tif
    return (g.get('tmp_dir') + '/' + prefix + str(uuid.uuid4()) + extension).encode('utf-8')

def create_tmp_file(string_value, prefix='', extension=''):
    filename = tmp_filename(prefix, extension)
    text_file = open(filename, "w")
    text_file.write(string_value)
    text_file.close()
    return filename
