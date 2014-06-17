from geostats import GeoStats


layer = {
    # the stored UID in the GeoMetadata database
    "uid" : "MODIS:test",

    }
#
# geostats = {
#     "code" : "226",
#     "query": "SELECT * FROM gaul0_3857 WHERE adm0_code IN ('226') ",
#     "statistics" : "all",
#     "save_stats" : True
#
# }
#
# geostats = {
#     "query_condition" : {
#         "column_filter" : "adm1_code",
#         "select" : "distinct(adm1_code)",
#         "from"   : "gaul1_3857",
#         "where"  : "adm0_code IN ('226')"
#     },
#     "save_stats" : True
# }
#
# geostats = {
#     "name" : "gaul2",
#     "query_condition" : {
#         "column_filter" : "adm2_code",
#         "select" : "distinct(adm2_code)",
#         "from"   : "gaul2_3857",
#         "where"  : "adm0_code IN ('226')"
#     },
#     "save_stats" : True
# }


geostats = {
    "name" : "gaul2",
    "geojson" : {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[43.0224609375,2.3943223575350774],[43.0224609375,3.623071326235699],[44.60449218749999,3.623071326235699],[44.60449218749999,2.3943223575350774],[43.0224609375,2.3943223575350774]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[46.07666015625,5.397273407690917],[46.38427734375,8.711358875426512],[50.25146484375,8.798225459016358],[46.73583984375,4.937724274302492],[46.07666015625,5.397273407690917]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[42.9345703125,5.878332109674327],[44.12109374999999,8.928487062665504],[44.89013671875,7.079088026071731],[43.70361328125,4.806364708499998],[42.9345703125,5.878332109674327]]]}}]},
    "save_stats" : False
}

gs = GeoStats()
gs.stats_layer_json(layer, geostats)
