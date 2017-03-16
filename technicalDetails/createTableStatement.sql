$ mysql.server start

mysql -u root
show databases;
create database xudatabase;
use xudatabase
show tables;


create table articles (pmid int, abstract text);
insert into articles values (1, 'testAbstract');


create table recommend_articles (entry_date datetime, user_id int, source_pmid int, pmid_1 int, pmid_2 int,pmid_3 int,pmid_4 int,pmid_5 int,pmid_6 int,pmid_7 int,pmid_8 int,pmid_9 int,pmid_10 int,score_1 float(7,6),score_2 float(7,6),score_3 float(7,6),score_4 float(7,6),score_5 float(7,6),score_6 float(7,6),score_7 float(7,6),score_8 float(7,6),score_9 float(7,6),score_10 float(7,6));


create table user_articles (user_id int, pmid int, abstract text, created datetime, deleted datetime, last_modified datetime);

insert into user_articles values (1, -1, 'blood cancer cell experiment yeast test',curdate(), NULL,curdate());

create table last_pmid (record_date datetime, user_id int)

insert into recommend_articles
values 
(1, 
curdate(), 
1, 
1, 
900001, 
900002,
900003,
900004,
900005,
900006,
900007,
900008,
900009,
900010,
0.10009,
0.10008,
0.10007,
0.10006,
0.10005,
0.10004,
0.10003,
0.10002,
0.10001,
0.10000);


insert into recommend_articles
values 
(3, 
curdate() - interval 1 day, 
2, 
2, 
203001, 
203002,
203003,
203004,
203005,
203006,
203007,
203008,
203009,
203020,
0.20009,
0.20008,
0.20007,
0.20006,
0.20005,
0.20004,
0.20003,
0.20002,
0.20001,
0.20000);