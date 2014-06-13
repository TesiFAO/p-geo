import sys
from flask import Flask, make_response, request, current_app
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import request
from flask import Response
from random import randrange
import random
from datetime import timedelta, datetime
import json
import csv

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../../')
    from utils import log, config

try:
    from postgresql.crowddata.crowddata import DBCrowddata
except Exception, e:
    sys.path.append('../../')
    from postgresql.crowddata.crowddata import DBCrowddata

config = config.Config('crowddata_postgresql')
database = config.get('database')
print database
db = DBCrowddata(database)
l = log.Logger()


class RandomData:

    def __init__(self):
        return None

    def date(self, start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def int(selfself, minimum, maximum):
        return randrange(minimum, maximum)

    def double(self, minimum, maximum):
        return random.uniform(minimum, maximum)

randomdata = RandomData()
lat = randomdata.double(41.7, 42.0)
lon = randomdata.double(12.40, 12.50)
for i in range(1, 3):
    d1 = datetime.strptime('1/1/2014 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('12/31/2014 4:50 AM', '%m/%d/%Y %I:%M %p')

    fulldate = randomdata.date(d1, d2)
    date = str(fulldate.year) + "-" + str(fulldate.month) + "-" + str(fulldate.day)


    price = randomdata.int(1.0, 50.0)
    untouchedprice = price

    commoditycode = randomdata.int(30, 32)
    # print "commoditycode" , commoditycode
    varietycode = commoditycode

    citycode = randomdata.int(0, 22)
    marketcode = citycode

    vendorcode = randomdata.int(0, 30)
    vendorname = "name" + str(vendorcode)

    munitcode = randomdata.int(0, 4)
    currencycode = 0

    if ( i % 10000 == 0 ):
        # lat = randomdata.double(4.0, 5.0)
        # lon = randomdata.double(4.0, 5.0)
        lat = randomdata.double(41.7, 42.0)
        lon = randomdata.double(12.40, 12.50)

    print lat
    print lon


    # print "price", price
    # print commoditycode
    # print varietycode
    # print citycode
    # print marketcode
    # print vendorcode
    # print vendorname

    data = [
        {
            "commoditycode" : str(commoditycode),
            "varietycode" : str(varietycode),
            "citycode" : str(citycode),
            "marketcode" : str(marketcode),
            "vendorcode" : str(vendorcode),
            "vendorname" :  str(vendorname),
            "munitcode" :  str(munitcode),
            "currencycode" :  str(currencycode),
            "date" : str(date),
            "fulldate" : str(fulldate),
            "price": price,
            "untouchedprice": untouchedprice,
            "lat" : lat,
            "lon" : lon
        }
    ]
    table= "data"

    # TODO: create a csv instead of an insert
    db.import_data(table, data)

    # csv_data = []
    # with open('/home/vortex/Desktop/eggs.csv', 'wb') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    # spamwriter.writerow(csv_data)