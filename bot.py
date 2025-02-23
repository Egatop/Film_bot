import telebot
from config import token
from logic import facts
from logic import DB_Manager
from translate import Translator
from config import db


from random import randint
import sqlite3 



user_facts = {}  
bot = telebot.TeleBot(token)

def translate_text(text, from_lang='en', to_lang='ru'):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    try:
        translated_text = translator.translate(text)
        return translated_text 
    except Exception:
        return f"не указано"

def send_facts(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    for index, fact in enumerate(facts):
        markup.add(telebot.types.InlineKeyboardButton(fact.text, callback_data=str(index)))
    bot.send_message(chat_id, "Выберите интересный факт:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    selected_index = int(call.data)  
    if 0 <= selected_index < len(facts):
        response = facts[selected_index].response
        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, "Выбранный факт недоступен.")

def senf_info(bot, message, row):
    overview = translate_text(row[7])
    if overview == 'QUERY LENGTH LIMIT EXCEEDED. MAX ALLOWED QUERY : 500 CHARS':
        overview = row[7]
    bot.send_message(message.chat.id, f'Название фильма: {row[1]}🎥\n\nДата выхода: {row[4]}📆\n\nКраткий сюжет📺:\n{overview}')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Здравствуй! тебя приветствует бот-киноман! выбери одну из следующих команд или же напиши название фильма, чтобы я попытался его найти:
                    /random - вывести случайный фильм из всего списка
                    /facts - узнать парочку интересных фактов о фильмах!
                    /genre - найти случайный фильм определённого жанра""")
    
@bot.message_handler(commands=['genre'])
def addtask_command(message):
    bot.send_message(message.chat.id,"Выбери жанр интерисующего фильма\nв ответном сообщении напиши цифру жанра")

    bot.send_message(message.chat.id,
"""1.Анимация
2.Приключения
3.Комедия
4.Боевик
5.Триллер
6.Драма
7.Романтика
8.Биография
9.История
10.Преступление
11.Тайна
12.Семья
13.Война
14.Фэнтези
15.Музыка
16.Ужасы
17.Спорт
18.Научная фантастика
19.Документальный фильм
20.Вестерн
21.Мюзикл
22.Фильм-нуар
23.Короткометражка
24.Новости""")
    
    bot.register_next_step_handler(message, promt)
    
def promt(message):
    promt1 = message.text
    movie = manager.get_film(int(promt1))
    date = manager.get_date(int(promt1),movie[1])
    overview = manager.get_overview(int(promt1),movie[1])
    if overview != 'не указано':
        overview = translate_text(overview)
    if overview == 'QUERY LENGTH LIMIT EXCEEDED. MAX ALLOWED QUERY : 500 CHARS':
        overview = manager.get_overview(int(promt1),movie[1])
    bot.send_message(message.chat.id, f'Название фильма: {movie[0]}🎥\n\nДата выхода: {date}📆\n\nКраткий сюжет📺:\n{overview}')

@bot.message_handler(commands=['random'])
def random_movie(message):
    con = sqlite3.connect("movie.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM movies ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)

@bot.message_handler(commands=['facts'])
def facts_command(message):
    send_facts(message.chat.id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("movie.db")
    with con:
        cur = con.cursor()
        cur.execute(f"select * from movies where LOWER(title) = '{message.text.lower()}'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Да, я знаю такой фильм!")
            senf_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"Хм, не припоминаю такого фильма...")

        cur.close()


manager = DB_Manager(db)

bot.infinity_polling()