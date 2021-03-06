import glob
import sys
import os
from osgeo import gdal
from ftplib import FTP
try:
    from utils import log, config, filesystem, ftp
except Exception, e:
    sys.path.append('../')
    from utils import log, config, filesystem, ftp


l = log.Logger('raster')

def list_subdatasets(target_dir, filename):
    """
    List the sub-datasets of a layer
    @param filename: Name of the layer to read
    @return: List of available sub-datasets for the given layer
    """
    gtif = gdal.Open(target_dir + '/' + filename)
    list = []
    sds = gtif.GetSubDatasets()
    for tmp in sds:
        list.append(tmp[0])
    return list

def extract_band(target_dir, band):
    """
    Extract a given band from a layer
    @param band: Number of the band to extract, starting from 0
    @return: Full path of the required band
    """
    l.info('extract band ' + target_dir)
    files = []
    out = []
    for fname in glob.glob(target_dir + '/*.hdf'):
        files.append(fname)
    for file in files:
        gtif = gdal.Open(file)
        sds = gtif.GetSubDatasets()
        try:
            out.append(sds[int(band) - 1][0])
        except Exception, e:
            l.error('Exception for file "' + file + '"\n' + e)
    return out

def modisDownloadExtractDelete(product, year, day, layer):

    c = config.Config('MODIS')
    filesystem.create_modis_structure(product, year, day)
    bands = c.get('bands')
    subfolders = c.get('subfolders')

    dir = c.get('ftp_dir') + '/' + product + '/' + year + '/' + day + '/'
    targetDir = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + subfolders['original'] + '/'
    file = layer
    local_file = os.path.join(targetDir, file)
    if not os.path.exists(local_file):
        try:
            l.info('Downloading layer "' + layer + '"')
            if not os.path.exists(local_file):
                l.info('Downloading: ' + local_file)
                ftp = FTP(c.get('ftp'))
                ftp.login()
                ftp.cwd(dir)
                ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
            else:
                l.info('Layer "' + layer + '" already exists. Skip.')
            ftp.quit()
            l.info('Download: done.')
        except Exception, e:
            l.error('Error while downloading layer: ' + layer)
            ftp.quit()
    else:
        l.info(local_file + ' already exists.')
    gtif = gdal.Open(local_file)

    for b in bands:
        band = filesystem.fix_band_name(gtif.GetSubDatasets()[int(bands[b])][0])
        out_file = c.get('targetDir') + '/' + product + '/' + year + '/' + day + '/' + b + '/' + subfolders['tmp'] + '/' + layer
        cmd = 'gdal_translate -q ' + band + ' ' + out_file
        try:
            if not os.path.exists(out_file):
                os.system(cmd)
                l.info('GDAL Translate: done. [' + layer + ']')
        except Exception, e:
            l.error('Error during GDAL Translate: ' + e)

def trmmDownloadExtractDelete(product, year, month, layer):

    c = config.Config('TRMM')
    filesystem.create_trmm_structure(product, year, month)
    subfolders = c.get('subfolders')

    dir = c.get('ftp_dir') + '/' + year + '/' + month + '/'
    targetDir = c.get('targetDir') + '/' + product + '/' + year + '/' + month + '/' + subfolders['original'] + '/'