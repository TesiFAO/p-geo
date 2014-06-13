import urllib2
import json
import uuid


class OSM:
    # i.e. http://nominatim.openstreetmap.org/search?q=135+pilkington+avenue,+birmingham&format=xml&polygon=1&addressdetails=1
    url_search = "http://nominatim.openstreetmap.org/search?"

    # i.e. http://nominatim.openstreetmap.org/reverse?format=json&lat=52.5487429714954&lon=-1.81602098644987&zoom=18&addressdetails=1
    url_reverse = "http://nominatim.openstreetmap.org/reverse?"

    q = ""
    limit = "50"
    format = "json"
    exclude_place_ids = []
    all_ids = []

    def __init__(self, limit="50", format="json"):
        try:
            self.limit = limit;
            self.format = format;
        except Exception, e:
            print "Exception: ", e

    def write_csv_crowddata(self, f, q, additional_parameters):
        try:
            force_exit = False;
            self.exclude_place_ids = [];
            while (True):
                url = self.url_search;
                url += "&q=" + q;
                url += "&limit=" + self.limit;
                url += "&format=" + self.format;
                url += additional_parameters;

                if ( len(self.exclude_place_ids) > 0 ):
                    s = ','.join(self.exclude_place_ids)
                    url += "&exclude_place_ids=" + s;

                print url
                req = urllib2.Request(url.encode("utf8"))

                response = urllib2.urlopen(req)
                result = json.loads(response.read())

                if ( len(result) > 0 ):
                    for x in result:
                        print x
                        if x["place_id"] in self.exclude_place_ids:
                            print "value: ", x["place_id"], "in the list -> exit"
                            force_exit = True;
                            break;
                        if x["place_id"] in self.all_ids:
                            print x["place_id"], "  is already in the list"
                            self.exclude_place_ids.append(x["place_id"])
                        else:
                            f.writerow([
                                uuid.uuid4(),
                                x["display_name"].encode('utf-8'),
                                x["type"].encode('utf-8'),
                                "en",
                                "true",
                                "true",
                                x["class"].encode('utf-8'),
                                x["place_id"],
                                ','.join(x["boundingbox"]),
                                x["lat"],
                                x["lon"],
                                ""
                            ])
                            self.exclude_place_ids.append(x["place_id"])
                            self.all_ids.append(x["place_id"])
                else:
                    break;
                if ( force_exit is True ):
                    break;
        except Exception, e:
            print e
