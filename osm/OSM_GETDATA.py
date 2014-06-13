from OSM import OSM
import csv

osm = OSM();
filename = "vendor_lazio.csv"
f = csv.writer(open(filename, "wb+"))

# header of the csv
f.writerow(["code", "name", "type", "lang", "shown", "onosm", "class", "place_id", "boundingbox", "lat", "lon", "geo"]);

# queries = ["Nairobi","Mombasa","Kisumu","Nakuru","Eldoret","Malindi","Marimanti","Imenti","Nyahururu","Kitale","Kakamega","Machakos","Kisii","Busia","Taveta","Loitokitok","Embu","Kitui","Chwele","Tharaka","Isiolo","Kajiado"]
queries = ["lazio"]

# filtering by Kenya
additional_parameters = "&countrycodes=it"
for q in queries:
    # q="nairobi,kenya"
    print "STARTING: ", q
    osm.write_csv_crowddata(f, q ,additional_parameters)
    osm.write_csv_crowddata(f, q +"[supermarket]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[mall]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[retail]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[marketplace]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[open-air20%market]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[street20%market]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[open20%market]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[the20%market]",additional_parameters)
    osm.write_csv_crowddata(f, q +"+[open-market]",additional_parameters)