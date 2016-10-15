USE costkeeper_main;

CREATE TABLE countries(
	country_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	country_name VARCHAR(20)
	PRIMARY KEY  (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE regions(
	regions_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	country_id VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE cities(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	region_id VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE streets(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE roles(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	admin BOOLEAN
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE users(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nickname VARCHAR(20),
	email VARCHAR(20),
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	role_id VARCHAR(20),
	avatar VARCHAR(20),
	password VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE shops(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	city_id INT UNSIGNED,
	street_id INT UNSIGNED,
	building VARCHAR(5)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE goods(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	barcode INT UNSIGNED UNIQUE,
	name VARCHAR(20),
	life VARCHAR(10),
	description TEXT,
	prod_country_id INT UNSIGNED,
	type_id INT UNSIGNED
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE costs(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	good_id INT UNSIGNED,
	shop_id INT UNSIGNED,
	currency_id INT UNSIGNED,
	cost_value FLOAT UNSIGNED
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE types_of_goods(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE currency(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	code VARCHAR(5) UNIQUE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE baskets(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	user INT UNSIGNED,
	creation_date TIMESTAMP,
	modify_date TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE basket(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	code VARCHAR(5) UNIQUE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;