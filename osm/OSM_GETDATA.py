from OSM import OSM
import csv

def get_data(inputcsv, outputcsv, iso2s):
    # ead csv with the cities
    osm = OSM();
    queries = []
    with open(inputcsv, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            queries.append(row[0].replace(" ", "+"))

    additional_parameters = "&countrycodes=" + iso2s
    f = csv.writer(open(outputcsv, "wb+"))
    f.writerow(["code", "name", "type", "lang", "shown", "onosm", "class", "place_id", "boundingbox", "lat", "lon", "geo"]);
    write_csv(osm, f, queries, additional_parameters)


def write_csv(osm, f, queries, additional_parameters):
    for q in queries:
        # q="nairobi,kenya"
        print "STARTING: ", q
        osm.write_csv_crowddata(f, q +"[supermarket]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[mall]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[retail]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[marketplace]",additional_parameters)
        # osm.write_csv_crowddata(f, q +"+[open-air20%market]",additional_parameters)
        # osm.write_csv_crowddata(f, q +"+[street20%market]",additional_parameters)
        # osm.write_csv_crowddata(f, q +"+[open20%market]",additional_parameters)
        # osm.write_csv_crowddata(f, q +"+[the20%market]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[open-market]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[butcher]",additional_parameters)
        osm.write_csv_crowddata(f, q +"+[fruit]",additional_parameters)

# loading data
#get_data('kenya_cities.csv', "markets_kenya.csv", "KE")
#get_data('bangladesh_cities.csv', "markets_bangladesh.csv", "BD")
#get_data('italy_regions.csv', "markets_italy.csv", "IT")
#get_data('yemen_cities.csv', "markets_yemen.csv", "YE")
get_data('somalia_cities.csv', "markets_somalia.csv", "SO")