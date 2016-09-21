USE costkeeper_main;

CREATE TABLE user(
	id INT UNIQUE,
  shop_name VARCHAR(20)
);

CREATE TABLE shops(
	id INT UNIQUE,
  shop_name VARCHAR(20)
);

CREATE TABLE regions(
	id INT UNIQUE,
  region_name VARCHAR(20)
);

CREATE TABLE cities(
	id INT UNIQUE,
  city_name VARCHAR(20),
  zip_code MEDIUMINT UNSIGNED,
  region_id INT
);

CREATE TABLE goods(
	id INT UNSIGNED UNIQUE,
	barcode INT UNSIGNED
);

CREATE TABLE baskets(
	id INT UNIQUE,
	user INT
);

CREATE TABLE basket(
	id INT UNIQUE
);

CREATE TABLE costs(
	id INT UNIQUE
);