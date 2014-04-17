import sys

try:
    from utils import log, config, ftp, filesystem
except Exception, e:
    sys.path.append('../')
    from utils import log, config, ftp, filesystem


# Parameters
year = '2014'
month = '04'
product = '3B42RT'

# Initiate utilities
c = config.Config('TRMM')
l = log.Logger('TRMM')
subfolders = c.get('subfolders')

# Get layers list
nasa_layers = ftp.listDir(c.get('ftp'), c.get('ftp_dir') + year + month + '/')

# Filter the 1day at midnight ones
fao_layers = filter(lambda x: '00.7.1day.' in x, nasa_layers)

# Create TRMM structure in the filesystem
filesystem.create_trmm_structure(product, year, month)

# Download TRMM
targetDir = c.get('targetDir') + '/' + product + '/' + year + '/' + month + '/' + subfolders['original'] + '/'
ftp.downloadList(c.get('ftp'), c.get('ftp_dir') + year + month + '/', targetDir, fao_layers)