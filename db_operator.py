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

def _check_existence(item , data_from_db):
    print(data_from_db.split(','))
    if data_from_db == None:
        return False
    elif item in data_from_db.split(','):
        print(item, data_from_db.split(','))
        return True
    else:
        return False



def db_users_films_add(user_chat_id, item, category):
    try:
        print(user_chat_id)
        conn = sqlite3.connect('users_films.db')
        cur = conn.cursor()
        cur.execute("SELECT {} FROM users_films WHERE userchatid = {}".format(category, user_chat_id))
        result_from_db = cur.fetchall()
        item_from_db = result_from_db[0][0]
        print(item_from_db)
        if _check_existence(item, item_from_db):
            return False
        else:
            res = str(item_from_db) + ',' + str(item)
            cur.execute(f"UPDATE users_films SET {category} = ? WHERE userchatid = ?", (res, user_chat_id))
        cur.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(e)
