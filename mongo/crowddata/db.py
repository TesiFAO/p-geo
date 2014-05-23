import sys
import pymongo
import datetime
from bson import json_util
import time
import calendar

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

config = config.Config('crowddata')
client = pymongo.MongoClient(config.get('database').get('connection'))
database = config.get('database').get('db')
document_data = config.get('database').get('document').get('data')
document_date = config.get('database').get('document').get('date')

def insertData(json):
    # insert (unique) date
    date = [int(s) for s in json['date'].split(',')]
    json["date"] = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

    date = [int(s) for s in json['fulldate'].split(',')]
    json["fulldate"] = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))

    # insert data json in data
    mongo_commons.insert(client, database, document_data, json)
    cursor = client[database][document_date].find({ "date" : json["date"]}).count()
    print cursor
    if ( cursor <= 0):
        insertDate({ "date" : json["date"] })



def insertDate(json):
    mongo_commons.insert(client, database, document_date, json)

def find(collection):
    cursor = client[database][collection].find().sort('name', pymongo.ASCENDING)
    return json_util.dumps(cursor)

def find_date():
    result = []
    min = client[database][document_date].find({}, { "_id":0 }).sort("date", 1).limit(1);
    max = client[database][document_date].find({}, { "_id":0 }).sort("date", -1).limit(1);
    result.append({"min":min})
    result.append({"max":max})
    return json_util.dumps(result)

def aggregate_by(json):
    cursor = client[database][document_data].aggregate(json)
    return json_util.dumps(cursor)


def find_by(json):
    cursor = client[database][document_data].find(json)
    return json_util.dumps(cursor)


def query_map(codes, startdate, enddate, bbox):
    q = []

    # where
    q.append({'$match': {'commoditycode' : { '$in' : codes}}})
    q.append({'$match': {'date': {"$gte": startdate, "$lte": enddate}}})

    # bbox (where)
    if ( bbox != '*' ):
        d = dict()
        print "bbox: " + d
        q.append({'$match': {'geo': {'$geoIntersects': {'$geometry': d}}}})

    # $groupby
    #j.append({ '$group' : { '_id': {'vendorcode': "$vendorcode", 'vendorname': "$vendorname", 'varietycode': "$varietycode", 'varietyname': "$varietyname",  'muunitssymbol':"$munitsymbol", 'geo' : "$geo"}, 'price' : { '$avg' : "$price" } } })
    q.append({ '$group' : { '_id': {'commoditycode': "$commoditycode", 'vendorname': "$vendorname", 'commodityname': "$commodityname", 'varietycode': "$varietycode", 'varietyname': "$varietyname",  'munitsymbol':"$munitsymbol", 'currencysymbol':"$currencysymbol",'geo' : "$geo"}, 'price' : { '$avg' : "$price" } } })


    # q.append({ '$project' : {'commodityname': '$commodityname' }} )


    # sort
    #q.append({ '$sort': { 'price': 1 } })
    return aggregate_by(q)


def query_timeserie_breakdown(codes, startdate, enddate, bbox):
    q = []

    # where
    q.append({'commoditycode' : { '$in' : codes}})
    q.append({'date': {"$gte": startdate, "$lte": enddate}})

    # bbox (where)
    if ( bbox != '*' ):
        d = dict()
        print "bbox: " + d
        q.append({'geo': {'$geoIntersects': {'$geometry': d}}})


    # orderby
    q.append({ '$sort': [{ 'varietyname' : 1 }, { 'date' : -1 }]})

    #q[0] is neeeded because find takes an object and not an array
    result = find_by(q[0])
    return format_timeserie(result)


def query_timeserie(codes, startdate, enddate, bbox):
    q = []

    # where
    q.append({'$match': {'commoditycode' : { '$in' : codes}}})
    q.append({'$match': {'date': {"$gte": startdate, "$lte": enddate}}})

    # bbox (where)
    if ( bbox != '*' ):
        d = dict()
        print "bbox: " + d
        q.append({'$match': {'geo': {'$geoIntersects': {'$geometry': d}}}})

    # $groupby
    q.append({ '$group' : { '_id': {'varietyname': "$varietyname", 'varietycode': "$varietycode",'date': "$date"}, 'price' : { '$avg' : "$price" } } })

    # sort
    q.append({ '$sort': { '_id' : 1}})

    print q
    #q[0] is neeeded because find takes an object and not an array
    return json_util.dumps(format_timeserie(aggregate_by(q)))


def format_timeserie(result):
    series = [] #data, name
    serie = {}
    serie['name'] = ""
    serie['data'] = []
    r = json_util.loads(result)
    print r
    for v in r["result"]:
        # create new serie
        if ( v['_id']['varietyname'] != serie['name'] ):
            if ( serie['name'] != ''): series.append(serie)
            serie = {}
            serie['data'] = []
            serie['name'] = v['_id']['varietyname']
            date = v['_id']['date']
            data = [calendar.timegm(date.utctimetuple()) * 1000, v['price']]
            serie['data'].append(data)
        else:
            date = v['_id']['date']
            # data = [time.mktime(date.timetuple()), v['price']]
            data = [ calendar.timegm(date.utctimetuple()) * 1000, v['price']]
            serie['data'].append(data)
    # this is to appena the last serie
    series.append(serie)
    #print series
    return series


def query_builder(groupby, sort):
    jsonGroupby = { '$group' : { '_id': {'vendorcode': '$vendorcode', 'vendorname': '$vendorname', 'varietycode': '$varietycode', 'geo' : '$geo'}, 'price' : { '$avg' : '$price' } }};
    jsonSort = { '$sort': { 'price': 1 } }
    jsonGeo = {}
    j = []
    j.append(groupby)
    j.append(sort)
    print j
    cursor = client[database][document_data].aggregate(j)
    return json_util.dumps(cursor)


def query_build_where(fields):
    return "TODO"

def query_build_groupy(fields, rule, field):
    fs = {}
    for  f in fields:
        fs[f] = '$' + f
    return { '$group' : { '_id': fs, field : { '$'+ rule +'' : '$'+field+'' } }}

def query_build_sort(filed, order):
    return { '$sort': { filed: order } }

# insertData('{"munitsymbol": "Kg","vendorcode": 1,"varetyname": "Variety of Avocado","munitcode": 1,"untouchedprice": 324,"marketcode": 1,"nationcode": 1,"currencycode": 1,"commoditycode": 1,"price": 3.6,"commodityname": "Avocado","citycode": 1,"varetycode": 1,"date": new Date(2014, 05, 15, 17, 57, 37),"dateupload": new Date(),   "geo": {"type": "Point","coordinates": [38.36402,-3.40193]},"vendorname": "Vendor of Nairobi","kind": 0,"notes": "","currencysymbol": "KSh","quantity": 90}');

# /d = dumps('{{ $group : { _id: {vendorcode: "$vendorcode", vendorname: "$vendorname", varietycode: "$varietycode", varietyname: "$varietyname",  muunitssymbol:"$munitsymbol"}, price : { $avg : "$price" } } }, { $sort: { price: 1 } }')
# print d
# print r

# jsonGroupby= query_build_groupy(['vendorcode', 'vendorname', 'varietycode'], 'avg', 'price')
# jsonSort= query_build_sort('price', 1)
# r = query_builder(jsonGroupby,jsonSort)
# print r

# enddate = datetime.datetime(2015, 8, 4)
# startdate = datetime.datetime(2003, 8, 4)
# print query_map([1], startdate, enddate);

# date = parser.parse("2014,1,1")
# print date
# #post = {"author": "Mike", "text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}
# insert = {"commoditycode": 1,"commodityname": "Avocado","varietycode": 1,"varietyname": "Variety of Avocado","quantity": 90,"price": 3.6,"currencycode": 1,"currencysymbol": "KSh","untouchedprice": 324,"munitcode": 1,"munitsymbol": "Kg","nationcode": 1,"citycode": 1,"marketcode": 1,"vendorcode": 1,"vendorname": "Vendor of Nairobi","geo": {    "type": "Point",    "coordinates": [38.36402,-3.40193    ]},"date": "2014,1,1","notes": "","kind": 0}
# insert['date'] = parser.parse("2014,1,1")
# insertData(insert)
