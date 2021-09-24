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

def _check_exist(user_chat_id, item, data_from_db):
    watch_list_status = False
    willwatch_list_status = False
    viewed_list_status = False
    if item in data_from_db[0][1]:
        watch_list_status = True
    elif item in data_from_db[0][2]:
        willwatch_list_status = True
    elif item in data_from_db[0][3]:
        viewed_list_status = True
    return (watch_list_status, willwatch_list_status, viewed_list_status)

def db_movied_add_to_user_list(user_chat_id, item, operator):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users_films WHERE userchatid={user_chat_id}")
    result_from_db = cur.fetchall()
    print(result_from_db)
    result_exist_status = _check_exist(user_chat_id, item, result_from_db)
    print(result_exist_status)
    result_message = ''
    if result_exist_status[0] == True:
        result_message = 'Still in watch list'
    elif result_exist_status[1] == True:
        result_message = 'Still in will watch list'
    elif result_exist_status[2] == True:
        result_message = 'Still in viewed list'
    else:
        if result_from_db == None or result_from_db == '':
            pass
        else:
            if operator == 'watch':
                res = ''
                for i in result_from_db[0][1].split(','):
                    if i != '':
                        res += i + ','
                res += str(item) + ','
            elif operator == 'willwatch':
                res = ''
                for i in result_from_db[0][2].split(','):
                    if i != '':
                        res += i + ','
                res += str(item) + ','
            elif operator == 'viewed':
                res = ''
                for i in result_from_db[0][3].split(','):
                    if i != '':
                        res += i + ','
                res += str(item) + ','
            print(operator)
            cur.execute(f"UPDATE users_films SET {operator}='{res}' WHERE userchatid={user_chat_id}")
        result_message = f'Added to {operator} list'
    cur.close()
    conn.commit()
    conn.close()
    print(result_message)
    return result_message

def dell_from_db(user_chat_id, item):
    conn = sqlite3.connect('users_films.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users_films WHERE userchatid={user_chat_id}")
    result_from_db = cur.fetchall()
    print(result_from_db)
    result_exist_status = _check_exist(user_chat_id, item, result_from_db)
    print(result_exist_status)
    res_all_list = list()
    res_all = ''
    if result_exist_status[0] == True:
        for i in result_from_db[0][1].split(','):
            if i != '':
                if i != item:
                    res_all += i + ','
        res_all_list.append(res_all)
        res_all_list.append(result_from_db[0][2])
        res_all_list.append(result_from_db[0][3])
    elif result_exist_status[1] == True:
        res_all = ''
        for i in result_from_db[0][2].split(','):
            if i != '':
                if i != item:
                    res_all += i + ','
        res_all_list.append(result_from_db[0][1])
        res_all_list.append(res_all)
        res_all_list.append(result_from_db[0][3])
    elif result_exist_status[2] == True:
        res_all = ''
        for i in result_from_db[0][3].split(','):
            if i != '':
                if i != item:
                    res_all += i + ','
        res_all_list.append(result_from_db[0][1])
        res_all_list.append(result_from_db[0][2])
        res_all_list.append(res_all)

    print(res_all_list)
    cur.execute(f"UPDATE users_films SET watch='{res_all_list[0]}',willwatch='{res_all_list[1]}',viewed='{res_all_list[2]}' WHERE userchatid={user_chat_id}")
    cur.close()
    conn.commit()
    conn.close()
    return 'Cleared'
