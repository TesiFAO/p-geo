CREATE TABLE city (
  code varchar(10) primary key,
  name varchar(80),
  type varchar(10),
  shown boolean
);
SELECT AddGeometryColumn('city','geo','4326','POINT',2);
CREATE INDEX city_gix ON city USING GIST (geo);


CREATE TABLE market (
  code varchar(10) primary key,
  -- use foreign key for data integrity?
  parentcode varchar(10) references city(code),
  name varchar(80),
  shown boolean
);

CREATE TABLE vendor (
  code varchar(10) primary key,
  -- use foreign key for data integrity?
  parentcode varchar(10) references market(code),
  name varchar(80),
  type varchar(10),
  shown boolean
);
SELECT AddGeometryColumn('vendor','geo','4326','POINT',2);
CREATE INDEX vendor_gix ON vendor USING GIST (geo);

CREATE TABLE commodity (
  code varchar(10) primary key,
  name varchar(80),
  shown boolean,
  divisor double precision
);

CREATE TABLE variety (
  code varchar(10) primary key,
  -- use foreign key for data integrity?
  -- use parentcode?
  parentcode varchar(10) references commodity(code),
  name varchar(80),
  shown boolean,
  divisor double precision
);

CREATE TABLE munit (
  code varchar(10) primary key,
  name varchar(80),
  shown boolean
);

CREATE TABLE gaul0 (
  code varchar(10) primary key,
  name varchar(80)
);


CREATE TABLE data (
  -- TODO: use gaulcode
  gaul0code varchar(10),
  vendorcode varchar(10),
  munitcode varchar(10),
  varietycode varchar(10),
  price double precision,
  untouchedprice double precision,
  date date,
  fulldate date,
  note text
);
SELECT AddGeometryColumn('data','geo','4326','POINT',2);
CREATE INDEX data_gix ON vendor USING GIST (geo);

-- cambiamenti:
--
-- notes in note
-- fulldate serve?
--
--
--
-- {
-- "munitsymbol" : "kg",
--  "vendorcode" : 1,
--  "varietyname" : "Variety of Cooking Bananas",
--  "fulldate" : ISODate("2014-05-20T12:27:16Z"),
--  "munitcode" : 1, "timezone" : "GMT+00:00",
--  "untouchedprice" : 324,
--  "marketcode" : 1,
--  "varietycode" : 0,
--  "nationcode" : 1,
--  "currencycode" : 1,
--  "commoditycode" : 12,
--  "price" : 40,
--  "commodityname" :
--  "Cooking Bananas",
--  "citycode" : 0,
--  "marketname" :
--  "Market of Nairobi",
--  "date" : ISODate("2013-11-02T00:00:00Z"),
--  "geo" : { "type" : "Point", "coordinates" : [ -2.3076443553579207, 31.647173039367384 ] },
--  "vendorname" : "Vendor of Nairobi",
--  "kind" : 0,
--  "notes" : "",
--  "currencysymbol" : "KSh",
--  "quantity" : 22 }






-- { "munitsymbol" : "kg", "vendorcode" : 1, "varietyname" : "Variety of Cooking Bananas", "fulldate" : ISODate("2014-05-20T12:27:16Z"), "munitcode" : 1, "timezone" : "GMT+00:00", "untouchedprice" : 324, "marketcode" : 1, "varietycode" : 0, "nationcode" : 1, "currencycode" : 1, "commoditycode" : 12, "price" : 40, "commodityname" : "Cooking Bananas", "citycode" : 0, "marketname" : "Market of Nairobi", "date" : ISODate("2013-11-02T00:00:00Z"), "geo" : { "type" : "Point", "coordinates" : [ -2.3076443553579207, 31.647173039367384 ] }, "vendorname" : "Vendor of Nairobi", "kind" : 0, "notes" : "", "currencysymbol" : "KSh", "quantity" : 22 }
