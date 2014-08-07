#!/bin/bash
#dropdb -U fenix faostat
#createdb -U fenix faostat-search --encoding='utf-8'
#psql  -U fenix faostat-search -c "CREATE EXTENSION pg_trgm;"
psql -U fenix faostat-search -f faostat.sql
