#! /usr/bin/env python2.7
# Prints statistics about newspaper website

import psycopg2

"""1. What are the most popular three articles of all time?
Which articles have been accessed the most?
 Present this information as a sorted list with the most
  popular article at the top.
"""
try:
    conn = psycopg2.connect("dbname=news")
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()
try:
    cur.execute("""select a.title, b.c  from articles a
     right join
    (select replace(path, '/article/','') as path , count(*) c from log
     group by path order by c desc limit 4) as
      b on a.slug = b.path where title is not NULL order by c desc;""")
except:
    print("I can't SELECT ")

rows = cur.fetchall()
print("The 3 most popular articles are:")
for row in rows:
    print(row[0] + '  -- ' + str(row[1]) + ' Views')
conn.close()


"""2. Who are the most popular article authors of all time?
That is, when you sum up all of the articles each author has written,
 which authors get the most page views? Present this as a sorted
  list with the most popular author at the top.
"""
try:
    conn = psycopg2.connect("dbname=news")
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()
try:
    cur.execute("""select name, sum  from authors a, author_views v
     where a.id = v.author order by sum desc;""")
except:
    print("I can't SELECT ")

rows = cur.fetchall()
print("\nThe  most popular article authors are:")
for row in rows:
    print(row[0] + '  -- ' + str(row[1]) + ' Views')
conn.close()

"""3. On which days did more than 1% of requests lead to errors?
The log table includes a column status that indicates the HTTP
 status code that the news site sent to the user's browser.
 (Refer to this lesson for more information about the idea
  of HTTP status codes.)
"""
try:
    conn = psycopg2.connect("dbname=news")
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()
try:
    cur.execute("""select e.count as errors, ok.count as successful,
     round(cast(e.count as decimal)/ok.count*100, 2) as errrate, ok.d from
      (select count(status), time::date d from log where status != '200 OK'
       group by d) as e
    , (select count(*), status, time::date d from log where status = '200 OK'
     group by d, status) as ok
     where e.d = ok.d and  round(cast(e.count as decimal)/ok.count*100, 2) >1;
     """)
except:
    print("I can't SELECT ")

rows = cur.fetchall()
print("\nThe  days in which the error rate went above 1 percent are:")
for row in rows:
    print(str(row[3]) + '  -- ' + str(row[2]) + '%')
conn.close()
