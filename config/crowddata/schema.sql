CREATE TABLE market (
  -- use foreign key for data integrity?
  code varchar(36),
  name text,
  type text,
  lang varchar(2),
  shown boolean,
  onosm boolean,
  class text,
  place_id varchar(64),
  boundingbox varchar(100),
  lat float,
  lon float,
  geo geometry,
  CONSTRAINT market_pkey PRIMARY KEY (code),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(geo) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geo) = 'POINT'::text OR geo IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(geo) = 4326)
);
CREATE INDEX market_gix ON market USING GIST (geo);
CREATE INDEX market_ix  ON market(code, lang);

CREATE TABLE vendor (
  parentcode char(36) references market(code)
) INHERITS (market);
CONSTRAINT vendor_pkey PRIMARY KEY (code),
CREATE INDEX vendor_gix ON vendor USING GIST (geo);


CREATE TABLE saletype (
  code varchar(36),
  name varchar(80),
  lang varchar(2),
  CONSTRAINT saletype_pkey PRIMARY KEY (code)
);
CREATE INDEX saletype_id  ON saletype(code, lang);


CREATE TABLE commodity (
  version varchar(10),
  code varchar(36),
  basic_element_flag varchar(2),
  name text,
  lang varchar(2),
  CONSTRAINT commodity_pkey PRIMARY KEY (code)
);
CREATE INDEX commodity_ix ON commodity(code, lang);

CREATE TABLE variety (
  parentcode varchar(36) references commodity(code),
  code varchar(36),
  -- use foreign key for data integrity?
  -- use parentcode?
  name text,
  lang varchar(2),
  CONSTRAINT variety_pkey PRIMARY KEY (code)
);
CREATE INDEX variety_ix ON variety(code, lang);
CREATE INDEX variety2_ix ON variety(code);

CREATE TABLE munit (
  code varchar(36) primary key,
  name text,
  fullname text,
  description text,
  lang varchar(2),
  shown boolean
);
CREATE INDEX munit_ix ON munit(code, lang);


CREATE TABLE currency (
  code varchar(36) primary key,
  name varchar(80),
  fullname varchar(80),
  lang varchar(2),
  shown boolean
);
CREATE INDEX currency_ix ON currency(code, lang);

CREATE TABLE gaul0 (
  code varchar(36) primary key,
  name text
);

CREATE TABLE users (
  id varchar(36) primary key,
--   username varchar(80),
  firstname varchar(80),
  lastname varchar(80),
  password varchar(80),
  contact varchar(80)
);
CREATE INDEX users_ix ON users(id, password);

CREATE TABLE data (
--   id should be increased automatically
  id BIGSERIAL PRIMARY KEY,
  -- TODO: use gaulcode (retrieved at runtime)
  gaul0code varchar(36),
  marketcode varchar(36) references market(code),
  munitcode varchar(36) references munit(code),
  currencycode varchar(36) references currency(code),
  commoditycode varchar(36) references commodity(code),
  varietycode varchar(36) references variety(code),
  saletypecode varchar(36) references saletype(code),
  quantity double precision,
  price double precision,
  untouchedprice double precision,
  date date,
  fulldate timestamp,
  note text,
  userid varchar(80),
  vendorname varchar(80),
  vendorcode varchar(36),
  lat float,
  lon float,
  geo geometry,
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(geo) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geo) = 'POINT'::text OR geo IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(geo) = 4326)
);
CREATE INDEX data_gix ON data USING GIST (geo);
CREATE INDEX date_ix ON data(date);
CREATE INDEX date2_ix ON data(date ASC);
CREATE INDEX date3_ix ON data(date DESC);
CREATE INDEX variety_date_vendorcode_ix on data(varietycode, vendorcode, date);
-- complex index on date, commoditycode
CREATE INDEX map_ix ON data(commoditycode, date);
CREATE INDEX map2_ix ON data(commoditycode, varietycode, date, munitcode, currencycode, geo, price);

-- CLUSTER data USING date_ix;
-- VACUUM ANALYZE data;
VACUUM FULL ANALYZE data;

-- Import data

-- market
COPY market FROM '/work/crowddata/markets_kenya.csv' DELIMITER ',' CSV HEADER;
COPY market FROM '/work/crowddata/markets_bangladesh.csv' DELIMITER ',' CSV HEADER;
COPY market FROM '/work/crowddata/italy.csv' DELIMITER ',' CSV HEADER;
UPDATE market SET geo = ST_GeomFromText('POINT(' || lon || ' ' || lat || ')',4326);

-- commodity
COPY commodity FROM '/work/crowddata/HS_2012.csv' DELIMITER ',' CSV HEADER;

-- variety
-- COPY variety FROM '/work/crowddata/variety.csv' DELIMITER ',' CSV HEADER;

-- munit
COPY munit FROM '/work/crowddata/munit.csv' DELIMITER ',' CSV HEADER;

-- currency
COPY currency FROM '/work/crowddata/currency.csv' DELIMITER ',' CSV HEADER;

-- saletype
COPY saletype FROM '/work/crowddata/saletype.csv' DELIMITER ',' CSV HEADER;



-- Triggers
-- CREATE FUNCTION my_trigger_function() RETURNS trigger AS'
-- BEGIN
-- END' LANGUAGE 'plpgsql';
--
-- CREATE TRIGGER my_trigger AFTER INSERT ON test FOR EACH STATEMENT EXECUTE PROCEDURE my_trigger_function()