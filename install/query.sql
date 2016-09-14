use costkeeper_main;

create table shops(
	id int unique
);

create table regions(
	id int unique,
    region_name char(20)
);

create table cities(
	id int unique,
    city_name char(20),
    zip_code int,
    region_id int
);

create table goods(
	id int unique,
	barcode int
);

create table baskets(
	id int unique,
	user int
);

create table baskets_contain(
	id int unique
);

create table good_costs(
	id int unique
);