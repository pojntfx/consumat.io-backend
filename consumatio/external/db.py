import sqlite3
import datetime
from consumatio.external.logger import get_logger_instance

logger = get_logger_instance()


class Database():
    def __init__(self):
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()

        cur.execute(
            '''CREATE TABLE IF NOT EXISTS cache(query text UNIQUE, body text, last_changed date)'''
        )

        con.commit()
        con.close()

    def cache(self: object, query: str, body: str) -> None:
        """
        Cache the provided query and the respective result in the database.
        :param query: <str> Tmdb query string
        :param body: <str> Response of the query 
        """
        logger.info("Query was successfully saved database")
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()

        cur.execute(
            '''INSERT INTO CACHE VALUES (:query, :body, :last_changed)''', {
                "query": query,
                "body": body,
                "last_changed": datetime.date.today()
            })

        con.commit()
        con.close()

    def is_cached(self: object, query: str) -> bool:
        """
        Checks if a query is cached in the database.
        :param query: <str> Tmdb query string
        :return: <bool> Returns true if the query is cached, else false 
        """
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()

        cur.execute('SELECT * FROM cache WHERE query=:query', {"query": query})

        result = cur.fetchall()

        if len(result) != 0 and datetime.date.today() - datetime.timedelta(
                days=10) < datetime.datetime.strptime(result[0][2],
                                                      '%Y-%m-%d').date():

            con.commit()
            con.close()
            logger.info("Query exists in database")
            return True
        else:
            if len(result) != 0 and datetime.date.today() - datetime.timedelta(
                    days=10) > datetime.datetime.strptime(
                        result[0][2], '%Y-%m-%d').date():
                cur.execute('''DELETE FROM cache WHERE query=:query''',
                            {"query": query})

            con.commit()
            con.close()
            logger.info("Query doesnt exists in database")
            return False

    def get_from_cache(self: object, query: str) -> str:
        """
        Get body of a query out of the database if the query was cached.
        :param query: <str> tmdb query string
        :return: <str> body of query
        """
        logger.info("Query load from database")
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT body from cache WHERE query=:query',
                    {"query": query})

        result = cur.fetchall()

        con.commit()
        con.close()

        return result[0][0]