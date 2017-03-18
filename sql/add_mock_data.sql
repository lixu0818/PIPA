insert into recommend_articles
values 
(1, 
1, 
10001,
curdate(), 
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
(2,
1, 
10002, 
curdate() - interval 1 day, 
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

insert into user_articles values (1, -1, 'blood cancer cell experiment yeast test',curdate(), NULL,curdate());

insert into articles values (1, 'testAbstract');