import telebot
from telebot import types
import logging
#projet imports
from db_operator import *
from info_searcher import *

#set logger settings
logging.basicConfig(level=logging.INFO, filename='logs.log', format=('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
logger = logging.getLogger()
# set bot
with open('token.txt') as f:
    token = f.read().split('\n')[0]
bot = telebot.TeleBot(token)
#set main menu
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True)
main_menu_keyboard.row('Search','By rating','Profile')
#set profile menu
profile_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True)
profile_menu_keyboard.row('Watch', 'Will watch', 'Viewed', 'Back')
#set inline menu
inline_markup_film_parameters = types.InlineKeyboardMarkup(row_width=3)
watch = types.InlineKeyboardButton("Watch", callback_data='watch')
weillwatch = types.InlineKeyboardButton("WillWatch", callback_data='willwatch')
viewed = types.InlineKeyboardButton("Viewed", callback_data='viewed')
clear = types.InlineKeyboardButton("Clear", callback_data='clear')
inline_markup_film_parameters.add(watch, weillwatch, viewed, clear)

@bot.message_handler(commands=['start'])
def _start(message):
    bot.send_message(message.chat.id, 'Hello, {}'.format(message.chat.username), reply_markup=main_menu_keyboard)
    db_users_write((message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.id))

@bot.message_handler(content_types=['text'])
def dialog_operator(message):
    lower_text_user_request = message.text.lower()
    if lower_text_user_request == 'search':
        bot.send_message(message.chat.id, 'Enter title name.')
        bot.register_next_step_handler(message, _find_by_titlename)
    elif lower_text_user_request == 'by rating':
        bot.send_message(message.chat.id, 'How many titles you want?')
        bot.register_next_step_handler(message, _find_by_rating)

    elif lower_text_user_request == 'profile':
        bot.send_message(message.chat.id, 'Your profile.',reply_markup=profile_menu_keyboard)
    elif lower_text_user_request == 'watch':
        result_movie_list = db_return_users_films(message.chat.id, 'watch')
        for i in result_movie_list:
            for i2 in i:
                bot.send_photo(message.chat.id, i2[4], caption=f"Title name:{i2[1]}\nYear:{i2[2]}\nGenres:{i2[3]}\nRating:{i2[5]}\nContent rating:{i2[6]}\nImdb_id:{i2[0]}", reply_markup=inline_markup_film_parameters)
    elif lower_text_user_request == 'will watch':
        result_movie_list = db_return_users_films(message.chat.id, 'willwatch')
        for i in result_movie_list:
            for i2 in i:
                bot.send_photo(message.chat.id, i2[4], caption=f"Title name:{i2[1]}\nYear:{i2[2]}\nGenres:{i2[3]}\nRating:{i2[5]}\nContent rating:{i2[6]}\nImdb_id:{i2[0]}", reply_markup=inline_markup_film_parameters)
    elif lower_text_user_request == 'viewed':
        result_movie_list = db_return_users_films(message.chat.id, 'viewed')
        for i in result_movie_list:
            for i2 in i:
                bot.send_photo(message.chat.id, i2[4], caption=f"Title name:{i2[1]}\nYear:{i2[2]}\nGenres:{i2[3]}\nRating:{i2[5]}\nContent rating:{i2[6]}\nImdb_id:{i2[0]}", reply_markup=inline_markup_film_parameters)
    elif lower_text_user_request == 'back':
        bot.send_message(message.chat.id, 'Main menu',reply_markup=main_menu_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'watch':
        if call.message.caption == None:
            st = str(call.message.text)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        else:
            st = str(call.message.caption)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        result_ans = db_movied_add_to_user_list(call.from_user.id, imdb_id, 'watch')
        bot.answer_callback_query(callback_query_id=call.id, text=result_ans)

    elif  call.data == 'willwatch':
        if call.message.caption == None:
            st = str(call.message.text)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        else:
            st = str(call.message.caption)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        result_ans = db_movied_add_to_user_list(call.from_user.id, imdb_id, 'willwatch')
        bot.answer_callback_query(callback_query_id=call.id, text=result_ans)

    elif call.data == 'viewed':
        if call.message.caption == None:
            st = str(call.message.text)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        else:
            st = str(call.message.caption)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        result_ans = db_movied_add_to_user_list(call.from_user.id, imdb_id, 'viewed')
        bot.answer_callback_query(callback_query_id=call.id, text=result_ans)
    elif call.data == 'clear':
        if call.message.caption == None:
            st = str(call.message.text)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        else:
            st = str(call.message.caption)
            imdb_id = st.split('\n')[-1].split(':')[-1]
        result_ans = dell_from_db(call.from_user.id, imdb_id)
        bot.answer_callback_query(callback_query_id=call.id, text=result_ans)


def _find_by_titlename(message):
    try:
        result = search_by_titlename(message.text)
        if result.get('Data') == '' or len(result.get('Data')) == 0:
            result_keywords = search_by_keywords(message.text)
            if result_keywords == '' or len(result_keywords) == 0:
                bot.send_message(message.chat.id, 'We can`t find this film. Sory.')
            else:
                for i in result_keywords.get('Movie Keyword Filter'):
                    imdb_id = i.get('imdb_id')
                    db_result = db_movie_check(imdb_id)
                    if len(db_result) == 0 or db_result == '' or db_result == None or db_result == False:
                        result_api_search = search_by_imdb_id(imdb_id)
                        item = result_api_search.get('Data')
                        title_name = item.get('title')
                        title_year = item.get('year')
                        title_imdb_id = item.get('imdb_id')
                        title_rating = item.get('rating')
                        title_content_rating = item.get('content_rating')
                        title_poster = item.get('image_url')
                        if 'banner' in item:
                            title_poster = item.get('banner')
                        elif 'poster' in item:
                            title_poster = item.get('poster')
                        elif 'image_url' in item:
                            title_poster = item.get('image_url')
                        title_genres = ''
                        for i in item.get('gen'):
                            title_genres += i.get('genre') + ', '
                        try:
                            bot.send_photo(message.chat.id, title_poster, caption=f'Title name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                            db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
                        except Exception as e:
                            logger.error(e)
                            bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                            db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
                            continue
                    else:
                        try:
                            bot.send_photo(message.chat.id, f'{db_result[0][4]}', caption=f'Title name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)
                        except Exception as e:
                            logger.error(e)
                            bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)


        else:
            for i in result.get('Data'):
                title_name = i.get('title')
                imdb_id = i.get('imdb_id')
                db_result = db_movie_check(imdb_id)
                if db_result == False:
                    result_api_search = search_by_imdb_id(imdb_id)
                    item = result_api_search.get('Data')
                    title_name = item.get('title')
                    title_year = item.get('year')
                    title_imdb_id = item.get('imdb_id')
                    title_rating = item.get('rating')
                    title_content_rating = item.get('content_rating')
                    title_poster = item.get('image_url')
                    if 'banner' in item:
                        title_poster = item.get('banner')
                    elif 'poster' in item:
                        title_poster = item.get('poster')
                    elif 'image_url' in item:
                        title_poster = item.get('image_url')
                    title_genres = ''
                    for i in item.get('gen'):
                        title_genres += i.get('genre') + ', '
                    try:
                        bot.send_photo(message.chat.id, title_poster, caption=f'Title name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                        db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
                    except Exception as e:
                        logger.error(e)
                        bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                        db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
                        continue
                else:
                    try:
                        bot.send_photo(message.chat.id, f'{db_result[0][4]}', caption=f'Title name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)
                    except Exception as e:
                        logger.error(e)
                        bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)
    except Exception as e:
        logger.error(e)
        logger.debug('find by titlename')

def _find_by_rating(message):
    result_top_by_rating_json = search_by_rating().get('Movie Order By Rating')
    for i in range(int(message.text)):
        imdb_id = result_top_by_rating_json[i].get('imdb_id')
        db_result = db_movie_check(imdb_id)
        if db_result == False or len(db_result) == 0:
            result_api_search = search_by_imdb_id(imdb_id)
            item = result_api_search.get('Data')
            title_name = item.get('title')
            title_year = item.get('year')
            title_imdb_id = item.get('imdb_id')
            title_rating = item.get('rating')
            title_content_rating = item.get('content_rating')
            title_poster = item.get('image_url')
            if 'banner' in item:
                title_poster = item.get('banner')
            elif 'poster' in item:
                title_poster = item.get('poster')
            elif 'image_url' in item:
                title_poster = item.get('image_url')
            title_genres = ''
            for i in item.get('gen'):
                title_genres += i.get('genre') + ', '
            try:
                bot.send_photo(message.chat.id, title_poster, caption=f'Title name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
            except Exception as e:
                logger.error(e)
                bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{title_name}\nYear:{title_year}\nGenres:{title_genres}\nRating:{title_rating}\nContent rating:{title_content_rating}\nImdb_id:{imdb_id}', reply_markup=inline_markup_film_parameters)
                db_movie_write((title_imdb_id, title_name, title_year, title_genres, title_poster, title_rating, title_content_rating))
                continue
        else:
            try:
                bot.send_photo(message.chat.id, f'{db_result[0][4]}', caption=f'Title name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)
            except Exception as e:
                logger.error(e)
                # bot.send_message(message.chat.id, f'Poster is unreadeble.\nTitle name:{db_result[0][1]}\nYear:{db_result[0][2]}\nGenres:{db_result[0][3]}\nRating:{db_result[0][5]}\nContent rating:{db_result[0][6]}\nImdb_id:{db_result[0][0]}', reply_markup=inline_markup_film_parameters)




def main():
    bot.polling()

if __name__ == '__main__':
    main()
