

#How to install MySQLdb (Python data access library to MySQL) on Mac OS X#Install Brew

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install mysql

pip install MySQL-python

python -c "import MySQLdb"

#if compile problem:
(Edit ~/.profile: (Might not be necessary in Mac OS X 10.10)

nano ~/.profile
Copy and paste the following two line

export PATH=/usr/local/mysql/bin:$PATH
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
Save and exit. Afterwords execute the following command:
source  ~/.profile
)

Run the following on the command line :

$ mysql.server start

mysql -u root
show databases;
create database xudatabase;
use xudatabase
show tables;
create table testtable (id int);
insert into testtable values (1);
select * from testtable;
drop table testtable;

create table articles (pmid int, abstract text);
insert into articles values (1, 'testAbstract');
commit;

create table recommend_articles (entry_date datetime, user_id int, source_pmid int, pmid_1 int, pmid_2 int,pmid_3 int,pmid_4 int,pmid_5 int,pmid_6 int,pmid_7 int,pmid_8 int,pmid_9 int,pmid_10 int,score_1 float(7,6),score_2 float(7,6),score_3 float(7,6),score_4 float(7,6),score_5 float(7,6),score_6 float(7,6),score_7 float(7,6),score_8 float(7,6),score_9 float(7,6),score_10 float(7,6));

select * from recommend_articles;

create table user_articles (user_id int, pmid int, abstract text, created datetime, deleted datetime, last_modified datetime);

insert into user_articles values (1, 10001, ‘’’’’’’testAbstract’,curdate(), NULL,curdate());

#/ autocomplete
truncate xxx;