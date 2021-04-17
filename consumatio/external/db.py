import sqlite3
import datetime

def cache(query, body):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS cache(query text UNIQUE, body text, last_changed date)''')

    cur.execute('''INSERT INTO CACHE VALUES (:query, :body, :last_changed)''', {"query": query, "body": body, "last_changed": datetime.date.today()})

    con.commit()
    con.close()

def is_cached(query):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS cache(query text UNIQUE, body text, last_changed date)''')

    cur.execute('SELECT * FROM cache WHERE query=:query', {"query": query})

    result = cur.fetchall()
    print(result)

    last_changed = result[0][2]

    if len(result) != 0 and datetime.date.today() - datetime.timedelta(days = 10) > datetime.datetime.strptime(last_changed, '%Y-%m-%d').date():
        con.commit()
        con.close()
        return True
    else:
        con.commit()
        con.close()
        return False