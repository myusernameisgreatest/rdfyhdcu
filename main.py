import telebot
from telebot import types
import time
import random
import psycopg2
import schedule
from conf import host,user,password,db_name

bot=telebot.TeleBot('6147893827:AAGpotEVgnoK4Savpc_M1ns6UQcWyuWO4rI')

class Beda:
    id = '1'
    __connection = None
    #st=True
    message='Привет'

    def init_db(self):  # проверка существования нужной таблицы, в противном случае - создание
        #connection.autocommit = True
        if self.__connection is None:
            self.__connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with self.__connection as connection:  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
            with self.__connection.cursor() as cursor:  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
                pass

    def list_messages(self, message, id): # получение данных
        with self.__connection as connection:  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
            with connection.cursor() as cursor:  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
                cursor.execute("""SELECT text FROM message WHERE id=%s;""", (id))
                self.__connection.commit
                bot.send_message(message.chat.id, cursor.fetchone())
                #cursor.close()
                #self.__connection.close()

    def job(self, message):
        id = str(random.randrange(1, 10, 1))
        self.list_messages(self, message, id)
        print('проверка3')


class Alfa:
    st = True

    def nstop(self,message):
        self.st = True
        bot.send_message(message.chat.id, str(self.st) + ' Я еще не начал')

    def got(self,message):
        stage = Beda
        self.st = False
        print('проверка ', self.st)
        schedule.every().minutes.at(":01").do(stage.job, stage, message)
        while self.st == False:
            schedule.run_pending()
            time.sleep(1)

    def stop(self,message):
        print('проверка2')
        self.st = True
        bot.send_message(message.chat.id, str(self.st) + ' OK')


@ bot.message_handler(commands=['start'])
def website(message):
    knopka = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)#resize_keyboard - подстраивается под размер экрана, row_width - количество кнопок в ряду
    start=types.KeyboardButton('ГОТОВ')
    stap=types.KeyboardButton('СТОП')
    knopka.add(start, stap)
    bot.send_message(message.chat.id, 'Если готов, нажми кнопку внизу', reply_markup=knopka)

@bot.message_handler()
def gotova(message):
    stage=Beda
    levl=Alfa
    stage.init_db(stage)

    if message.text == 'СТОП' and levl.st == True:
        levl.nstop(levl,message)

    if message.text == 'ГОТОВ':
        levl.got(levl,message)

    if message.text == 'СТОП' and levl.st == False:
        levl.stop(levl,message)

bot.polling(none_stop=True)