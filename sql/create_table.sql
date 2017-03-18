create table articles (id int not null auto_increment primary key, pmid int, abstract text);

create table last_pmid 
	(id int not null auto_increment primary key, 
	record_date datetime, 
	pmid int);

create table recommend_articles 
(	id int not null auto_increment primary key,
	entry_date datetime, user_id int, source_pmid int, 
	pmid_1 int, pmid_2 int,pmid_3 int,pmid_4 int,pmid_5 int,
	pmid_6 int,pmid_7 int,pmid_8 int,pmid_9 int,pmid_10 int,
	score_1 float(7,6),score_2 float(7,6),score_3 float(7,6),score_4 float(7,6),score_5 float(7,6),
	score_6 float(7,6),score_7 float(7,6),score_8 float(7,6),score_9 float(7,6),score_10 float(7,6),
	...
	foreign key (user_id) references users(id));

create table user_articles 
(	id int not null auto_increment primary key,
	user_id int, pmid int, title varchar(200), abstract varchar(2000), 
	created datetime, deleted datetime, lastmodified datetime,
	foreign key (user_id) references users(id));

create table users
(   id int not null auto_increment primary key,
	email varchar(60), 
	username varchar(60),
	first_name varchar(60),
	last_name varchar(60),
	created datetime,
	lastmodified datetime,
	password_hash varchar(128),
	is_admin tinyint,
	constraint uc_email unique (email),
	constraint uc_username unique (username) );	