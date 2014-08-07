-- CREATE TABLE stats.{{tablename}}  (
--     polygon_id  char(36),
--     label_en  text,
--     fromdate  date,
--     todate   date,
-- --  '1_1 (january_1)'
--     dekad  char(4),
--     hist json,
--     mean double,
--     min double,
--     max double,
--     sd double
-- );


CREATE TABLE stats.test  (
    polygon_id  char(36),
    label_en  text,
    fromdate  timestamp,
    todate   timestamp,
    dekad  char(4),
    hist json,
    mean double precision,
    min double precision,
    max double precision,
    sd double precision
);

INSERT INTO stats.test (polygon_id) VALUES ('test')