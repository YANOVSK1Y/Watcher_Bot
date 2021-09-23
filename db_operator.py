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

def _check_existence(item, list_to_check):
    if list_to_check and item in list_to_check:
        return True
    else:
        pass

def db_add_to_watch_list(user_chat_id, item):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT watch from users_films WHERE userchatid={user_chat_id}")
    print(user_chat_id)
    res_from_db = cur.fetchall()
    print(res_from_db)

    if item in res_from_db[0][0]:
        print(True)
    else:
        res = ''
        for i in res_from_db[0]:
            res += i + ','
        res += item
        cur.execute("UPDATE users_films SET watch=? WHERE userchatid = ?", (res, user_chat_id))
    cur.close()
    conn.commit()
    conn.close()

def db_add_to_willwatch_list(user_chat_id, item):
    pass


def db_add_to_viewed_list(user_chat_id, item):
    pass


def db_users_films_add(user_chat_id, item, category):
    try:
        conn = sqlite3.connect('users_films.db')
        cur = conn.cursor()
        # cur.execute("SELECT {} FROM users_films WHERE userchatid = {}".format(category, user_chat_id))
        cur.execute("SELECT * FROM users_films WHERE userchatid = {}".format(user_chat_id))

        result_from_db = cur.fetchall()


        # if _check_existence(item, item_from_db):
        #     return (False, message)
        # else:
        #     res = str(item_from_db) + '-' + str(item)
        #     cur.execute(f"UPDATE users_films SET {category} = ? WHERE userchatid = ?", (res, user_chat_id))
        cur.close()
        conn.commit()
        conn.close()

    except Exception as e:
        logger.error(e)
