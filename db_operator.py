import sqlite3

def db_movie_check(imdb_id):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM movies WHERE imdb_id='{}'""".format(imdb_id))
    result = cur.fetchall()
    cur.close()
    conn.close()
    if len(result) > 0:
        return result
    else:
        return False
def db_movie_write(imdb_id):
    pass

def db_movie_get(imdb_id):
    pass
