#!/bin/bash
#dropdb -U fenix crowddata
#createdb -U fenix crowddata --encoding='utf-8'
#psql  -U fenix crowddata -c "CREATE EXTENSION postgis;"
#
#psql -U fenix crowddata -f schema.sql

# iso3 ita
dropdb -U fenix cd-ita
createdb -U fenix cd-ita --encoding='utf-8'
psql  -U fenix cd-ita -c "CREATE EXTENSION postgis;"

psql -U fenix cd-ita -f schema.sql