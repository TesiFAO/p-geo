# Import Default shapefiles into the database

# GAUL0
shp2pgsql -W LATIN1 -I -s 4326 gaul0/g2008_0.shp spatial.g2008_0 | psql -U fenix pgeo