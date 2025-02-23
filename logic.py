import sqlite3
from config import db
import random


class DB_Manager:
    def __init__(self, database):
        self.database = database

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    def insert_project(self, data):
        sql = 'INSERT OR IGNORE INTO movies (title, budget, popularity, release_date, vote_average, vote_count, overview) values(?, ?, ?, ?, ?, ?, ?)'
        self.__executemany(sql, data)
    def get_film(self,genre):
        try:
            conn = sqlite3.connect('movie.db')
            cur = conn.cursor()
            cur.execute("""SELECT movie_id FROM movies_genres WHERE genre_id = ?""",(genre,))
            mv_id = cur.fetchall()
            number = random.randint(0, len(mv_id))
            cur.execute("""SELECT title FROM movies WHERE id = ?""",(mv_id[number][0],))
            mv = cur.fetchall()
            film = [mv[0][0],number]
            return film
        except Exception:
            a = ['не указано','не указано']
            return a
    def get_date(self,genre,number):
        try:
            conn = sqlite3.connect('movie.db')
            cur = conn.cursor()
            cur.execute("""SELECT movie_id FROM movies_genres WHERE genre_id = ?""",(genre,))
            mv_id = cur.fetchall()
            cur.execute("""SELECT release_date FROM movies WHERE id = ?""",(mv_id[number][0],))
            mv = cur.fetchall()
            return mv[0][0]
        except Exception:
            a = 'не указано'
            return a
    def get_overview(self,genre,number):
        try:
            conn = sqlite3.connect('movie.db')
            cur = conn.cursor()
            cur.execute("""SELECT movie_id FROM movies_genres WHERE genre_id = ?""",(genre,))
            mv_id = cur.fetchall()
            cur.execute("""SELECT overview FROM movies WHERE id = ?""",(mv_id[number][0],))
            mv = cur.fetchall()
            return mv[0][0]
        except Exception:
            a = 'не указано'
            return a


if __name__ == '__bot__':
    manager = DB_Manager(db)
    #manager.create_tables()
    manager.default_insert()

class Fact:
    def __init__(self, text, response):
        self.text = text
        self.response = response

facts = [
    Fact("Факт 1: Эти 3 фильма считаются самыми дорогими.", "Ответ на факт 1: Это такие фильмы как 1.Звездные войны VII: Пробуждение Силы    2.Форсаж 10   3.Аватар: Путь воды. Слишком дорого "),
    Fact("Факт 2: 3 фильма с самым высоким рейтингом на онлайн площадках", "Ответ на факт 2: 1:Побег из Шоушенка       2:Крёстный отец     3:Тёмный рыцарь. Мне кажется они переоценены а вы что думаете?"),
    Fact("Факт 3: 3 фильма которые считаются самыми ожидаемыми в 2025.", "Ответ на факт 3: 1:Громовержцы      2:Лило и Стич     3:28 лет спустя. Те кто из будещего здесь? Подтвердились ли ожиданния?"),
    Fact("Факт 4: 3 фильма которые считаются самыми провальными .", "Ответ на факт 4: 1:Клеопатра      2:Врата рая     3:От всего сердца. Эти 3 фильма даже мне боту тяжело смотреть"),
    Fact("Факт 5: 3 фильма которые считаются недеоцененными.", "Ответ на факт 5: 1:Меч короля Артура      2:Сквозь снег     3:Убийцы цветочной луны. Эх какие фильмы почему так с шедеврами"),
]