import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', format=('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
logger = logging.getLogger(__name__)

def db_movie_check(imdb_id):
    try:
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
    except DBError as e:
        logger.error(e)

def db_movie_write(data):
    # data = (imdb_id, name, year, genres, poster, rating, c_rating)
    try:
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO movies VALUES (?,?,?,?,?,?,?)", data)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(e)

def db_users_write(data):
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?,?,?,?)", data)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(e)

def _check_existence(item , data):
    result_data = []
    if item in data:
        for i in data:
            if i == item:
                continue
            else:
                result_data.append(i)
        return result_data
    else:
        res = str(data) + ', '
        return res


def db_users_films_watch(user_chat_id, item):
    try:
        print(user_chat_id)
        #data (userchatid, watch, willwatch, viewed)
        conn = sqlite3.connect('users_films.db')
        cur = conn.cursor()
        cur.execute("SELECT watch FROM users_films WHERE userchatid = {}".format(user_chat_id))
        result_from_db = cur.fetchall()
        item_from_db = result_from_db[0][0]
        print(item_from_db)
        res = str(item_from_db) + ', ' + str(item)

        print(res)
        cur.execute("UPDATE users_films SET watch = ? WHERE userchatid = ?", (res, user_chat_id))

        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(e)
