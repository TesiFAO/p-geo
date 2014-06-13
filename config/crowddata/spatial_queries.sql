EXPLAIN ANALYZE SELECT d.vendorcode,
ST_ClosestPoint(d.geo, ST_GeomFromText('POINT(0.1235 0.3521)',4326))
FROM data as d;
WHERE
ST_DWithin(d.geo, ST_GeomFromText('POINT(0.1235 0.3521)',4326), 4)
order by distance
limit 5;


<!-- closest vendors -->
EXPLAIN ANALYZE
SELECT vendorcode, vendorname,
       ST_Distance(geo::geography, 'SRID=4326;POINT(0.0 0.0)'::geography)/1000 as dist_km
FROM data
ORDER BY geo <-> 'SRID=4326;POINT(0.0 0.0)' limit 10;



<!-- closest vendors -->
EXPLAIN ANALYZE
SELECT vendorcode, vendorname,
       ST_Distance(geo::geography, 'SRID=4326;POINT(4.0 4.0)'::geography)/1000 as dist_km
FROM data
ORDER BY geo <-> 'SRID=4326;POINT(4.0 4.0)' limit 10;

EXPLAIN ANALYZE
SELECT vendorcode, vendorname,
       ST_Distance(geo::geography, 'SRID=4326;POINT(41.0 12.0)'::geography)/1000 as dist_km
FROM data
ORDER BY geo <-> 'SRID=4326;POINT(41.0 12.0)' limit 10;


<!-- closest vendors with best prices by variety -->
EXPLAIN ANALYZE
SELECT d.varietycode, d.vendorcode, avg(d.price)
FROM data d
WHERE vendorcode IN (
	SELECT vendorcode
	FROM data
	ORDER BY geo <-> 'SRID=4326;POINT(0.0 0.0)' limit 100
)
AND varietycode = '5'
AND date ='2014-01-01'
GROUP BY varietycode, vendorcode
;

EXPLAIN ANALYZE
SELECT d.varietycode, d.vendorcode, avg(d.price)
FROM data d
WHERE vendorcode IN (
	SELECT vendorcode
	FROM data
	ORDER BY geo <-> 'SRID=4326;POINT(0.0 0.0)' limit 100
)
AND varietycode = '5'
AND date <= ('2014-03-01')
AND date >= ('2014-03-01- '2 day'::INTERVAL)
GROUP BY varietycode, vendorcode ;