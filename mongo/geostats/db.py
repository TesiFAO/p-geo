import sys
import pymongo

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../')
    from utils import log, config

try:
    from mongo import mongo_commons
except Exception, e:
    sys.path.append('../')
    from mongo import mongo_commons

config = config.Config('geostatistics')
client = pymongo.MongoClient(config.get('geostats_datastore').get('connection'))
database = config.get('geostats_datastore').get('db')

"""
Delete Layer Metadata in mongodb
@param json: json data
@return: id
"""
def removeMetadata(layer, json):
    return mongo_commons.remove(client, database, layer, json)


"""
Insert Layer Statistics in tmongodb
@param json: json data
@return: id
"""
def insert_stats(layer, json):
    id = mongo_commons.insert(client, database, layer, json)
    if ( id is not None ): print "Data Inserted ", id
    return id


"""
Return entire collection
@param collection: collection
@return: collection
"""
def find(collection):
    return mongo_commons.find(client, database, collection, { "$query": {}, "$orderby": [{ "layertitle" : 1 }, {"date" : 1}]})


"""
Return entire collection
@param collection: collection
@param query: mongodb query
@return: collection
"""
def find_query(collection, query):
    return mongo_commons.find(client, database, collection, query)



"""
Return the document containing the layername
@param collection: collection (i.e. layer)
@param layername: layername stored in the db
@return: collection
"""
def find_by_layername(collection, layername):
    return mongo_commons.find(client, database, collection, { "$query": { "layername" : layername }, "$orderby": [{ "layertitle" : 1 }]});
