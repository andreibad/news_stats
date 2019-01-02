# news_stats
Project Title 
Page View Statistics

Description
This project will print some statistics from a newspaper website database.

Getting Started
Step 1) create views in news db (see Prerequisites section below)
Step 2) run 'python log_analysis.py'

Prerequisites
I created the following views in the news database:

create view author_views as select a.author, sum(b.c)  from articles a right join  
    (select replace(path, '/article/','') as path , count(*) c from log group by path ) as b 
    on a.slug = b.path where a.author is not  NULL group by a.author  order by sum desc
;


Built With
python 2.7
psycopg2 DB-API


Authors
Andrei Badulescu

