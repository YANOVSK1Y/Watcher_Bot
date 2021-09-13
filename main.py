import telebot
from telebot import types
import logging
#projet imports
from db_operator import *
from info_searcher import *


#test func
from test_fuctions import *


#set logger settings
logging.basicConfig(level=logging.INFO, filename='logs.log', format=('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
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

@bot.message_handler(content_types=['text'])
def dialog_operator(message):
    lower_text_user_request = message.text.lower()
    if lower_text_user_request == 'search':
        # result_search = test_film()
        # bot.send_message(message.chat.id, '1', reply_markup=inline_markup_film_parameters)
        result = db_movie_check('tt4154796')[0]
        if len(result) > 0:
            bot.send_photo(message.chat.id, result[4], caption=f'Title: {result[1]}\nYear: {result[2]}\nGenreL: {result[3]}', reply_markup=inline_markup_film_parameters)

    elif lower_text_user_request == 'trends':
        pass
    elif lower_text_user_request == 'profile':
        bot.send_message(message.chat.id, 'Your profile.Select option',reply_markup=profile_menu_keyboard)
    elif lower_text_user_request == 'back':
        bot.send_message(message.chat.id, 'Main menu',reply_markup=main_menu_keyboard)
        bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(lambda query: query.data in ["watch", "willwatch", "viewed"])
def _watch_btn(query):
    if query.data == "watch":
        bot.send_message(query.from_user.id, 'added to watch list')
    elif query.data == "willwatch":
        bot.send_message(query.from_user.id, 'added to willwatch list')
    elif query.data == "viewed":
        bot.send_message(query.from_user.id, 'added to viewed list  ')



def main():
    bot.polling()



if __name__ == '__main__':
    main()
