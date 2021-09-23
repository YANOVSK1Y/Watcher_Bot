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


def db_add_to_watch_list(user_chat_id, item):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT watch from users_films WHERE userchatid={user_chat_id}")
    print(user_chat_id)
    res_from_db = cur.fetchall()
    print(res_from_db)
    if res_from_db == None or res_from_db == '':
        return False
    else:
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
        return True

def db_add_to_willwatch_list(user_chat_id, item):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT willwatch from users_films WHERE userchatid={user_chat_id}")
    print(user_chat_id)
    res_from_db = cur.fetchall()
    print(res_from_db)
    if res_from_db == None or res_from_db == '':
        return False
    else:
        if item in res_from_db[0][0]:
            print(True)
        else:
            res = ''
            for i in res_from_db[0]:
                res += i + ','
            res += item
            cur.execute("UPDATE users_films SET willwatch=? WHERE userchatid = ?", (res, user_chat_id))
        cur.close()
        conn.commit()
        conn.close()
        return True


def db_add_to_viewed_list(user_chat_id, item):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT viewed from users_films WHERE userchatid={user_chat_id}")
    print(user_chat_id)
    res_from_db = cur.fetchall()
    if res_from_db == None or res_from_db == '':
        return False
    else:
        print(res_from_db)
        if item in res_from_db[0][0]:
            print(True)
        else:
            res = ''
            for i in res_from_db[0]:
                res += i + ','
            res += item
            cur.execute("UPDATE users_films SET viewed=? WHERE userchatid = ?", (res, user_chat_id))
        cur.close()
        conn.commit()
        conn.close()
        return True

def db_movied_add_to_user_list(user_chat_id, item, operator):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT {operator} FROM users_films WHERE userchatid={user_chat_id}")
    result_from_db = cur.fetchall()
    if result_from_db == None or result_from_db == '':
        pass
    else:
        if item in res_from_db[0][0]:
            return True
        else:
            res = ''
            for i in res_from_db[0]:
                res += i + ','
            res += item
            cur.execute(f"UPDATE users_films SET {operator}={res} WHERE userchatid={user_chat_id}")

    cur.close()
    conn.commit()
    comm.close()
    return Fasle
