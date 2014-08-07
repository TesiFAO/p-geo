#!/bin/bash
#dropdb -U fenix crowddata
#createdb -U fenix crowddata --encoding='utf-8'
#psql  -U fenix crowddata -c "CREATE EXTENSION postgis;"
#
#psql -U fenix crowddata -f schema.sql

# iso3 ita
dropdb -U fenix cd-ita
createdb -U fenix cd-ita --encoding='utf-8'
#psql  -U fenix cd-ita -c "CREATE EXTENSION postgis;"

psql  -U fenix cd-ita -c "CREATE EXTENSION postgis;CREATE EXTENSION pg_trgm;"

# pg_trgm is used for the <-> function

psql -U fenix cd-ita -f schema.sql



createdb -U fenix faostat --encoding='utf-8'
psql  -U fenix faostat -c "CREATE EXTENSION pg_trgm;"
psql -U fenix faostat -f faostat.sql
