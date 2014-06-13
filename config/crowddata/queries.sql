
EXPLAIN ANALYZE SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type,ST_AsGeoJSON(d.geo)::json As geometry, row_to_json(( SELECT l FROM ( SELECT c.name as commodityname, v.name  as varietyname, mu.name as munitname, cu.name as currencyname, avg(price) as price) As l)) As properties FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu WHERE d.commoditycode IN ('0')  AND d.date BETWEEN '2014-11-1' AND '2014-12-31' AND d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND d.currencycode = cu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en' GROUP BY c.name, v.name, mu.name, cu.name, d.geo ) As f ) As fc;



EXPLAIN ANALYZE SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type,ST_AsGeoJSON(d.geo)::json As geometry, row_to_json((
SELECT l FROM ( SELECT d.commoditycode as commodityname, d.varietycode  as varietyname, d.munitcode as munitname, d.currencycode as currencyname, avg(price) as price) As l)) As properties
FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu WHERE d.commoditycode IN ('31')  AND d.date BETWEEN '2014-11-1' AND '2014-12-31' AND d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND d.currencycode = cu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en' GROUP BY d.commoditycode, d.varietycode, d.munitcode, d.currencycode, d.geo ) As f ) As fc;


ST_Buffer(ST_GeomFromText('POINT(1 2)'), 10) As smallc


EXPLAIN ANALYZE SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type,ST_AsGeoJSON(d.geo)::json As geometry, row_to_json(( SELECT l FROM ( SELECT c.name as commodityname, v.name  as varietyname, mu.name as munitname, cu.name as currencyname, avg(price) as price) As l)) As properties FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu WHERE d.commoditycode IN ('31')  AND d.date BETWEEN '2014-11-1' AND '2014-12-31' AND d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND d.currencycode = cu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en'
AND ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo)
GROUP BY c.name, v.name, mu.name, cu.name, d.geo ) As f ) As fc;


EXPLAIN ANALYZE SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type,ST_AsGeoJSON(d.geo)::json As geometry, row_to_json(( SELECT l FROM ( SELECT c.name as commodityname, v.name  as varietyname, mu.name as munitname, cu.name as currencyname, avg(price) as price) As l)) As properties FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu WHERE ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo) AND d.commoditycode IN ('31')  AND d.date BETWEEN '2014-11-1' AND '2014-12-31' AND d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND d.currencycode = cu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en'
GROUP BY c.name, v.name, mu.name, cu.name, d.geo ) As f ) As fc;


select count(*) from data where  ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), geo);



EXPLAIN ANALYZE
SELECT c.name, v.name, mu.name, cu.name, d.lat, d.lon, avg(price)
FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu
WHERE ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo)
AND d.commoditycode IN ('3')
AND d.date BETWEEN '2014-09-1' AND '2014-12-31'
AND d.commoditycode = c.code AND d.varietycode = v.code
AND d.munitcode = mu.code
AND d.currencycode = cu.code
AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en'
GROUP BY c.name, v.name, mu.name, cu.name, d.lat, d.lon

EXPLAIN ANALYZE
SELECT count(*) FROM (
  SELECT c.name, v.name, mu.name, cu.name, d.lat, d.lon, avg(price)
  FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu
  WHERE ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo)
  AND d.commoditycode IN ('1','2','3')
  AND d.date = '2014-09-1'
  AND d.commoditycode = c.code AND d.varietycode = v.code
  AND d.munitcode = mu.code
  AND d.currencycode = cu.code
  AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en'
  GROUP BY c.name, v.name, mu.name, cu.name, d.lat, d.lon) as tmp;


EXPLAIN (ANALYZE, BUFFERS, TIMING, COSTS) SELECT c.name, v.name, mu.name, cu.name, d.lat, d.lon, avg(price) FROM data AS d, commodity AS c, variety AS v, munit AS mu, currency AS cu WHERE ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo) AND d.commoditycode IN ('31')  AND d.date BETWEEN '2014-05-1' AND '2014-12-31' AND d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND d.currencycode = cu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND cu.lang = 'en'
GROUP BY c.name, v.name, mu.name, cu.name, d.lat, d.lon;





<!-- no VIEW e' lenta -->
CREATE VIEW view_test_31_en AS
SELECT c.name as commodityname, v.name as varietyname, mu.name as munitname, d.date as date, d.lat as lat, d.lon as lon, d.geo as geo, d.price as price
FROM data AS d, commodity AS c, variety AS v, munit AS mu
WHERE d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND d.commoditycode IN ('31');

<!-- meglio MATERIALIZED VIEW, TODO how to handle on insert and update-->
CREATE MATERIALIZED VIEW view31 AS
SELECT c.name as commodityname, v.name as varietyname, mu.name as munitname, d.date as date, d.lat as lat, d.lon as lon, d.geo as geo, d.price as price
FROM data AS d, commodity AS c, variety AS v, munit AS mu
WHERE d.commoditycode = c.code AND d.varietycode = v.code AND d.munitcode = mu.code AND c.lang = 'en' AND v.lang = 'en' AND mu.lang = 'en' AND d.commoditycode IN ('31');

TODO: ADD REFRESH ON COMMMIT!!!!


EXPLAIN (ANALYZE, BUFFERS, TIMING, COSTS) SELECT commodityname, varietyname, munitname, lat, lon, avg(price) FROM view31 AS d WHERE ST_Contains(ST_GeomFromText('POLYGON((2.28515625 4.36832042087623, 2.28515625 6.140554782450308, 4.28466796875 6.140554782450308, 4.28466796875 4.36832042087623, 2.28515625 4.36832042087623))', 4326), d.geo)AND d.date BETWEEN '2014-05-1' AND '2014-12-31'
GROUP BY commodityname, varietyname, munitname, d.lat, d.lon;


EXPLAIN (ANALYZE, BUFFERS, TIMING, COSTS) SELECT commodityname, varietyname, munitname, lat, lon, avg(price) FROM view31 AS d WHERE d.date BETWEEN '2014-8-1' AND '2014-12-31'
GROUP BY commodityname, varietyname, munitname, d.lat, d.lon;




CREATE INDEX view_idx2 ON view31 USING GIST (geo);









