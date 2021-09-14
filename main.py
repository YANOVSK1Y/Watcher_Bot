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
main_menu_keyboard.row('Search','Trends','Profile')
#set profile menu
profile_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True)
profile_menu_keyboard.row('Watch', 'Will watch', 'Viewed', 'Back')
#set inline menu
inline_markup_film_parameters = types.InlineKeyboardMarkup(row_width=3)
watch = types.InlineKeyboardButton("Watch", callback_data='watch')
weillwatch = types.InlineKeyboardButton("WillWatch", callback_data='willwatch')
viewed = types.InlineKeyboardButton("Viewed", callback_data='viewed')
inline_markup_film_parameters.add(watch, weillwatch, viewed)


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
    elif lower_text_user_request == 'trends':
        pass

    elif lower_text_user_request == 'profile':
        bot.send_message(message.chat.id, 'Your profile.',reply_markup=profile_menu_keyboard)

    elif lower_text_user_request == 'back':
        bot.send_message(message.chat.id, 'Main menu',reply_markup=main_menu_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'watch':
        bot.answer_callback_query(callback_query_id=call.id, text='Added to watch list')
        db_users_films_watch('377812122', 'tt777777')
    elif  call.data == 'willwatch':
        bot.answer_callback_query(callback_query_id=call.id, text='Added to willwatch list')
    elif call.data == 'viewed':
        bot.answer_callback_query(callback_query_id=call.id, text='Added to viewed list')


def _find_by_titlename(message):
    result = search_by_titlename(message.text)
    if len(result.get('Result')) == 0:
        bot.send_message(message.chat.id, 'We don`t have this film. Sory.')
    try:
        for i in result.get('Result'):
            title_name = i.get('title')
            imdb_id = i.get('imdb_id')
            db_result = db_movie_check(imdb_id)
            if db_result == False:
                bot.send_message(message.chat.id, 'Searching in gobal base')
                result_api_search = search_by_imdb_id(imdb_id)
                ttitle_result = result_api_search.get(title_name)
                titleimdbid = ttitle_result.get('imdb_id')
                titlename = ttitle_result.get('title')
                titleyear = ttitle_result.get('year')
                titlegennres_nonsorted = ttitle_result.get('gen')
                titlegenres = str()
                for i in titlegennres_nonsorted:
                    titlegenres += i.get('genre') + ', '
                titleposter = ttitle_result.get('banner')
                titlerating = ttitle_result.get('rating')
                titlecontentrating = ttitle_result.get('content_rating')
                data = (titleimdbid, titlename, titleyear, titlegenres, titleposter, titlerating, titlecontentrating)
                db_movie_write(data)
                bot.send_photo(message.chat.id, titleposter, caption=f'Title name: |{titlename}|\nYear: |{titleyear}|\nGenres: {titlegenres}\nRating: {titlerating}\nCOntent rating: {titlecontentrating}', reply_markup=inline_markup_film_parameters)
            else:
                bot.send_photo(message.chat.id, f'{db_result[0][4]}', caption=f'Title name: |{db_result[0][1]}|\nYear: |{db_result[0][2]}|\nGenres: {db_result[0][3]}\nRating: {db_result[0][5]}\nContent rating: {db_result[0][6]}', reply_markup=inline_markup_film_parameters)

    except Exception as e:
        logger.ERROR(e)
        bot.send_message(message.chat.id, 'Woops, somesing go wrong. Try nex time.')



def main():
    bot.polling()

if __name__ == '__main__':
    main()
