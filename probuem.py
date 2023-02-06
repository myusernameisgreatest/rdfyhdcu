import telebot
import sqlite3

bot=telebot.TeleBot('6147893827:AAGpotEVgnoK4Savpc_M1ns6UQcWyuWO4rI')

__connection=None

def get_connection(): # проверка коннекшн, если ничего нет, создает подключение
    global __connection
    if __connection is None:
        __connection=sqlite3.connect('bd.db') #проверка существования бд
    return __connection

def init_db(force:bool=False): #проверка существования нужной таблицы, в противном случае - создание

    conn=get_connection() #СОЗДАНИЕ ПОДКЛЮЧЕНИЯ

    c=conn.cursor() #СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД

    if force:
        c.execute('DROP TABLE IF EXISTS messages') #УДАЛИТЬ ЕЕ, ЕСЛИ ПЕРЕДАН ФЛАЖОК ФОРС

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            message     TEXT NOT NULL
            )
    ''')

    conn.commit()  # сохранение изменений
    conn.close()

def add_message(user_id:int,text:str):
    conn=get_connection()
    conn = sqlite3.connect('bd.db', check_same_thread=False)
    c=conn.cursor()
    c.execute('INSERT INTO messages (user_id,message) VALUES (?,?)',(user_id,text)) #вызов курсора экзекьют, куда передается код для вставки
    conn.commit()
    conn.close()

def list_messages(user_id: int, limit: int=10): #вытаскивание из базы последних 10 сообщений
    conn = get_connection()
    conn = sqlite3.connect('bd.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT message FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ? ', (user_id, limit)) #ORDER BY id DESC - по возрастанию ид
    return c.fetchall()

@bot.message_handler(commands=['start']) #комманды
def my_messages(message): #метод
    r = list_messages(user_id=message.from_user.id, limit=10)
    for i in r:
        bot.send_message(message.chat.id, i, parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    slova = f'{message.text}'
    add_message(user_id=message.from_user.id, text=slova)

bot.polling(none_stop=True)