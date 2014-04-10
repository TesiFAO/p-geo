import sys, os
import httplib2
from urlparse import urlparse
from gsutils import url, prepare_upload_bundle
import postgis_utils


try:
    from utils import config, log
except Exception, e:
    sys.path.append('../../')
    from utils import config, log

class Geoserver():

    # TODO: as converntion all the layers/styles should be in lowercase?

    def __init__(self, conf="geoserver", disable_ssl_certificate_validation=False):
        """
        Initialize and configure the GeoSeerver.
        The GeoServer properties are set in conf="geoserver" (config/geoserver.json) by default
        """
        self.config = config.Config(conf)
        self.logger = log.Logger()

        # use as parameters
        service_url = self.config.get('resturl');
        username = self.config.get('username')
        password = self.config.get('password')

        self.service_url = service_url
        if self.service_url.endswith("/"):
            self.service_url = self.service_url.strip("/")
        self.http = httplib2.Http(
            disable_ssl_certificate_validation=disable_ssl_certificate_validation)
        self.username = username
        self.password = password
        self.http.add_credentials(self.username, self.password)
        netloc = urlparse(service_url).netloc
        self.http.authorizations.append(
            httplib2.BasicAuthentication(
                (username, password),
                netloc,
                service_url,
                {},
                None,
                None,
                self.http
            ))
        self._cache = dict()
        self._version = None


    def get(self, property):
        """
        "wmsurl"  : "http://localhost:9090/geoserver/wms" //used for wms request
        "resturl" : "http://localhost:9090/geoserver"     //used for rest request
        "datadir" : "/home/vortex/programs/tomcat_geoservers/data/" //datadir used to get the raster data
        "username" : "admin",
        "password" : "geoserver",
        "default_workspace" : "fenix"
        "debug" : true
        """
        return self.config.get(property)

    def publish_raster(self, input_raster, name, layertype='GEOTIFF', workspace='fenix', metadata=''):
        self.logger.info('raster: ' + input_raster)
        #cmd = "curl -u '"+ self.config.get('username') +":" + self.config.get('password') + "' -XPUT -H 'Content-type:image/tiff' -T "+ input_raster + " " + self.config.get('resturl') +"/workspaces/"+ workspace +"/coveragestores/"+ name +"/file.geotiff"
        return "published"

    def publish_coveragestore(self, name, data, workspace=None, overwrite=False ):
        if not overwrite:
            try:
                is_used = self.check_if_coverage_exist(name, workspace)
                if ( is_used == True ):
                        self.logger.warn("There is already a store named " + name)
                        return "There is already a store named " + name
                        #raise ConflictingDataError(msg)
            except Exception, e:
                # we don't really expect that every layer name will be taken
                pass

        if workspace is None:
            workspace = self.get_default_workspace()
        headers = {
            "Content-type": "image/tiff",
            "Accept": "application/xml"
        }

        archive = None
        ext = "geotiff"

        if isinstance(data, dict):
            # handle 'tfw' (worldimage)
            archive = prepare_upload_bundle(name, data)
            message = open(archive, 'rb')
            if "tfw" in data:
                headers['Content-type'] = 'application/archive'
                ext = "worldimage"
        elif isinstance(data, basestring):
            message = open(data, 'rb')
        else:
            message = data

        cs_url = url(self.service_url, ["workspaces", workspace, "coveragestores", name, "file." + ext])
        self.logger.info(cs_url)
        try:
            headers, response = self.http.request(cs_url, "PUT", message, headers)
            self._cache.clear()
            if headers.status != 201:
                #raise UploadError(response)
                self.logger.error('error 201: ' + response)
                return False
        finally:
            if hasattr(message, "close"):
                message.close()
                return True
            if archive is not None:
                 self.logger.error('call nlink(archive) : ' + archive)
                #nlink(archive)

    def delete_coveragestore(self, name, workspace=None,purge=True, recurse=True):
        if workspace is None:
            workspace = self.get_default_workspace()

        # TODO: it makes two, calls, so probably it's better just handle the delete code
        if self.check_if_coverage_exist(name):
            cs_url = url(self.service_url, ["workspaces", workspace, "coveragestores", name])
            self.logger.info(cs_url);
            #headers, response = self.http.request(cs_url, "DELETE")

            return self.delete(cs_url, purge, recurse)
        else:
            return "NO COVERAGE STORE AVAILABLE"

    def delete(self, rest_url, purge=False, recurse=False):
        """
        send a delete request
        """

        #params aren't supported fully in httplib2 yet, so:
        params = []

        # purge deletes the SLD from disk when a style is deleted
        if purge:
            params.append("purge=true")

        # recurse deletes the resource when a layer is deleted.
        if recurse:
            params.append("recurse=true")

        if params:
            rest_url = rest_url + "?" + "&".join(params)

        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        response, content = self.http.request(rest_url, "DELETE", headers=headers)
        self._cache.clear()

        self.logger.info(response)

        if response.status == 200:
            #return (response, content)
            return 'coverage uploaded'
        else:
            self.logger.error("Tried to make a DELETE request to %s but got a %d status code: \n%s" % (rest_url, response.status, content))
            #raise FailedRequestError("Tried to make a DELETE request to %s but got a %d status code: \n%s" % (rest_url, response.status, content))
            return ("Tried to make a DELETE request to %s but got a %d status code: \n%s" % (rest_url, response.status, content))

    def check_if_coverage_exist(self, name, workspace=None):
        if workspace is None:
            workspace = self.get_default_workspace()
        cs_url = url(self.service_url, ["workspaces", workspace, "coveragestores", name])
        response, content = self.http.request(cs_url, "GET")
        if response.status == 200:
            return True
        elif response.status == 404:
            return False
        return False

    def set_default_style(self, stylename, layername, enabled=True):
        """
        Method used to change the default style of a layer
        :param stylename: the name of the style to set ad default one
        :param layername: the name of the layer
        :param enabled: enable/disable the style
        :return:
        """
        # curl -v -u $GEOSERVER_PASSWORD -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>$DEFAULT_STYLE</name></defaultStyle><enabled>$ENABLED</enabled></layer>" $GEOSERVER_URL/rest/layers/$GEOSERVER_WORKSPACE:$NAME
        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        xml = "<layer><defaultStyle><name>{0}</name></defaultStyle><enabled>{1}</enabled></layer>".format(unicode(stylename).lower(),  unicode(str(enabled).upper()))
        cs_url = url(self.service_url, ["layers", layername])
        headers, response = self.http.request(cs_url, "PUT", xml, headers)
        if headers.status == 200:
            return True
        else:
            return False

    def publish_shapefile(self, input_shapefile, name, overwrite=False, workspace=None, projection=None, default_style=None, layertype=None, metadata=None):
        """
        :param input_shapefile:
        :param name:
        :param overwrite:
        :param workspace:
        :param projection:
        :param default_style:
        :param layertype:
        :param metadata:
        :return:
        """

        # TODO: check if it's a shp or zip
        '''
        if zip:
            unzip "in tmp to be removed"
        '''
        datastore = self.get_default_datastore()
        postgis_utils.import_shapefile(datastore, input_shapefile, name )

        # publish shapefile
        self.publish_postgis_table(datastore, name)
        return "published"

    def publish_postgis_table(self, datastore, name):
        """
        :param datastore: datastore stored in geoserver
        :param name: name of the table in postgis
        :return:
        """
        #curl -v -u admin:geoserver -XPOST -H "Content-type: text/xml" -d "<featureType><name>buildings</name></featureType>"
        #http://localhost:8080/geoserver/rest/workspaces/acme/datastores/nyc/featuretypes
        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        xml = "<featureType><name>{0}</name></featureType>".format(unicode(name).lower())
        cs_url = url(self.service_url, ["workspaces", datastore['workspace'], "datastores", datastore['datastore'], 'featuretypes'])
        headers, response = self.http.request(cs_url, "POST", xml, headers)
        self.logger.info(headers)
        if headers.status == 201:
            return True
        else:
            return False

    def checkIFDatastoreExist(self, name):
        print 'TODO'

    def get_default_workspace(self):
        return self.get('default_workspace')

    def get_default_datastore(self):
        default_datastore = self.config.get('default_datastore')
        print default_datastore
        datastore = self.config.get('datastores')
        for d in datastore:
            self.logger.info(d['datastore'] == default_datastore)
            return d
        return False

