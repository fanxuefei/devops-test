import psycopg2
import psycopg2.extras
conn = psycopg2.connect(database="postgres",user="postgres", password="z8asuidn", host="118.190.166.165", port="5432")
cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

cur.execute("SELECT *  from fs_host")
rows = cur.fetchall()

for row in rows:
   print ("ID = ", row)
conn.close()
