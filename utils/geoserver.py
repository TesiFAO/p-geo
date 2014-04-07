import sys

try:
    from utils import config as c
except Exception, e:
    sys.path.append('../')
    from utils import config as c

class Geoserver():

    def __init__(self):
        """
        Initialize and configure the geoserver. The geoserver properties are
        set in the geoserver.json file stored in the config folder.
        """
        self.config = c.Config('geoserver')

    def get(self, property):
        """
        "wmsurl"  : "http://localhost:9090/geoserver/wms" //used for wms request
        "resturl" : "http://localhost:9090/geoserver"     //used for rest request
        "datadir" : "/home/vortex/programs/tomcat_geoservers/data/" //datadir used to get the raster data
        "username" : "username",
        "password" : "password",
        "debug" : true
        """
        return self.config.get(property)