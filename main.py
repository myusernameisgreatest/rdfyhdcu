import telebot  # Бот
from telebot import types  # Кнопки
import time  # Задержки
import random  # Тут все понятно
import psycopg2  # PostgreSQL
from conf import host, user, password, db_name  # Для подключения к БД

bot = telebot.TeleBot('6147893827:AAGpotEVgnoK4Savpc_M1ns6UQcWyuWO4rI')  # Бот


class Beda:
    __connection = None  # Переменная для подключения

    def init_db(self):  # Задание параметров подключения к бд
        if self.__connection is None:  # Если не заданы параметры подключения
            self.__connection = psycopg2.connect(host=host, user=user,
                                                 password=password, database=db_name)
                                                    # Параметры подключения

    def list_messages(self, message, id):  # Получение данных и выдача
        with self.__connection as connection:  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
            with connection.cursor() as cursor:  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
                cursor.execute("""SELECT text FROM message WHERE id=%s;""", (id))
                                                # Выбор сообщения со случайным id
                bot.send_message(message.chat.id, cursor.fetchone())  # Отправка сообщения

    def job(self, message):  # Задание случайного id + получение данных, выдача
        with self.__connection as connection:  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
            with connection.cursor() as cursor:  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
                cursor.execute("""SELECT id FROM message ORDER BY id DESC LIMIT 1;""")
                                                # Выбор одного наибольшего значения id
                predel = cursor.fetchone()  # Переменная для наибольшего значения id
                chislo = predel[0] + 1  # Увеличиваем на единицу, чтобы диапазон включал
        id = str(random.randrange(0, chislo, 1))  # Задаем id
        self.list_messages(self, message, id)  # Получаем данные по id и выдаем
        print('проверка3')


class Alfa:
    st = True  # Для остановки цикла
    a = True  # Для исключения повторного срабатывания цикла, когда он уже запущен

    def nstop(self, message):  # В случае остановки, когда цикл еще не запущен
        bot.send_message(message.chat.id, 'Я еще не начал!')

    def got(self, message):  # При нажатии готов
        stage = Beda  # Класс с job
        self.st = False  # Цикл выполняется свободно
        print('проверка')
        if self.a == True:  # Если кнопка еще не нажата
            while True:
                self.a = False  # Кнопка нажата
                if self.st == True:  # Если был нажат стоп
                    print('проверка4')
                    self.a = True  # Кнопка не нажата
                    break
                stage.job(stage, message)  # Задание случайного id + получение данных, выдача
                time.sleep(3)  # Задержка
        else:
            bot.send_message(message.chat.id, 'Уже нажал!')  # При повторном нажатии

    def stop(self, message):  # В случае остановки цикла
        print('проверка2')
        self.st = True  # Заперет выполнения цикла
        bot.send_message(message.chat.id, 'OK')


@ bot.message_handler(commands=['start'])  # Создание кнопок по команде start
def website(message):
    knopka = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # resize_keyboard - подстраивается под размер экрана, row_width - количество кнопок в ряду
    start = types.KeyboardButton('ГОТОВ')
    stap = types.KeyboardButton('СТОП')
    knopka.add(start, stap)  # Добавление кнопок
    bot.send_message(message.chat.id, 'Если готов, нажми кнопку внизу', reply_markup=knopka)


@bot.message_handler()
def gotova(message):  # Реакция на сообщения
    stage = Beda  # init
    levl = Alfa  # По сообщениям
    stage.init_db(stage)  # Задание параметров подключения к бд

    if message.text == 'СТОП' and levl.st == True:  # Стоп при выполнении цикла
        levl.nstop(levl, message)

    if message.text == 'ГОТОВ':  # Если готов
        levl.got(levl, message)

    if message.text == 'СТОП' and levl.st == False:  # Стоп при выключенном цикле
        levl.stop(levl, message)


# Работа без остановки
bot.polling(none_stop=True)