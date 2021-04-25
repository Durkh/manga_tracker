import os
import psycopg2


def connect_db():

    conn = None
    try:
        conn = psycopg2.connect(host='localhost', database='mangas',
                                user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWD'))

    except (Exception, psycopg2.DatabaseError) as error:
        raise Exception(error)
    else:
        if conn is not None:
            return conn, conn.cursor()
        else:
            return None, None
