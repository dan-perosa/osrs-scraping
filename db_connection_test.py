import psycopg2

user='postgres.rrszvwnprphovamfvzrs'
password='Senhasupabase2!'
host='aws-0-us-west-1.pooler.supabase.com'
port=5432
dbname='postgres'

conn = psycopg2.connect(user=user,
                        password=password,
                        host=host,
                        port=port,
                        dbname=dbname)

cur = conn.cursor()

cur.execute('SELECT * FROM quests')

records = cur.fetchall()

print(records)