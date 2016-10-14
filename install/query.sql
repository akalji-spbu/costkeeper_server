USE costkeeper_main;

CREATE TABLE countries(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20)
);

CREATE TABLE regions(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20),
	country_id VARCHAR(20)
);

CREATE TABLE cities(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20),
	region_id VARCHAR(20)
);

CREATE TABLE streets(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20)
);

CREATE TABLE roles(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20),
	admin BOOLEAN
);

CREATE TABLE users(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
  nickname VARCHAR(20),
	email VARCHAR(20),
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	role_id VARCHAR(20),
	avatar VARCHAR(20),
	password VARCHAR(20)
);

CREATE TABLE shops(
	id INT UNSIGNED UNIQUE PRIMARY KEY,
	name VARCHAR(20),
	city_id INT UNSIGNED,
	street_id INT UNSIGNED,
	building VARCHAR(5)
);

