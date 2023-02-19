import requests
from bs4 import BeautifulSoup
import time
import random
import datetime
import psycopg2
from conf import host,user,password,db_name

class Super:
    sayt='https://www.google.ru/search?q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B2+%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B7%D0%BD%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%B5&newwindow=1&sxsrf=AJOqlzUYMY_AXixbjGjIsYJwKEyktMDX0Q%3A1676367414314&ei=NlbrY6fjEvKGwPAP5o-P2AE&ved=0ahUKEwin1vih25T9AhVyAxAIHebHAxsQ4dUDCBA&uact=5&oq=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B2+%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B7%D0%BD%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%B5&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIMCAAQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyEgguEMcBENEDEOoCELQCEEMYATIMCAAQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyEgguEMcBENEDEOoCELQCEEMYATISCC4QxwEQ0QMQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyDAgAEOoCELQCEEMYATIMCAAQ6gIQtAIQQxgBSgQIQRgASgQIRhgBUABYqjxgv0BoAXABeACAAQCIAQCSAQCYAQCgAQGwARTAAQHaAQYIARABGAE&sclient=gws-wiz-serp'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    current_converted_price = 0
    difference = 1
    pozdr=0
    name='имя'
    soname='фамилия'
    birthday='07-01-1995'
    __connection = None

    def __init__(self):
        self.current_converted_price=int(self.get_currency_price())

    def get_currency_price(self):
        full_page = requests.get(self.sayt, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "wob_t","class": "q8U8x"})
        return convert[0].text

    def chech_currency(self):
        currency = int(self.get_currency_price())
        if currency>=self.current_converted_price + self.difference:
            m=random.randrange(0, 10, 1)
            if m<3:
                print ("Потеплело, снимай шапку!")
            if m>=3 and m<6:
                print("Потеплело, снимай куртку!")
            if m>=6:
                print("Потеплело, снимай перчатки!")
            self.current_converted_price = currency
        elif currency<=self.current_converted_price - self.difference:
            m = random.randrange(0, 10, 1)
            if m < 3:
                print("Похолодало, надевай шапку!")
            if m >= 3 and m < 6:
                print("Похолодало, надевай куртку!")
            if m >= 6:
                print("Похолодало, надевай перчатки!")
            self.current_converted_price=currency
        now = datetime.datetime.now()
        print (now.strftime("%d-%m-%Y %H:%M"))
        data=now.strftime("%d-%m")
        if data=='15-02' and self.pozdr==0:
            print('С праздником!!!')
            self.pozdr=1
        if data==birthday:
            print('С днем рождения, '+name+' '+soname+'!!!')
        print('Температура воздуха в Краснознаменске сейчас '+str(currency)+' оС')
        time.sleep(300)
        self.chech_currency()

    def init_db(self, force: bool = False):  # проверка существования нужной таблицы, в противном случае - создание
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        #connection.autocommit = True
        if self.__connection is None:
            self.__connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        conn = self.__connection  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
        cursor = conn.cursor()  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД

        cursor.execute("SELECT version();")  # передача в метод execute запроса на получение версии сервера
        # print(f"Server version:{cursor.fetchone()}")  # fetchone возвращает кортеж или none, если запрос пустой

        if force:
            cursor.execute('DROP TABLE IF EXISTS birthday')  # УДАЛИТЬ ЕЕ, ЕСЛИ ПЕРЕДАН ФЛАЖОК ФОРС
            print("[INFO] Table was deleted")

        # cursor.execute("""CREATE TABLE birthday(
        #             id          serial PRIMARY KEY,
        #             myname      varchar NOT NULL,
        #             mysoname    varchar NOT NULL,
        #             dateof      varchar NOT NULL);""")
        print(cursor.fetchall())
        cursor.execute("""SELECT * FROM birthday""")
        print((f"Data:{cursor.fetchone()}"))
        print("[INFO] Table created successfully")
        self.__connection.commit
        cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")

    def add_message(self, soname: str, name: str, birthday: str):#добавление данных
        conn = self.__connection  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
        cursor = conn.cursor()  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
        n=self.name
        s=self.soname
        b=self.birthday
        cursor.execute("""INSERT INTO birthday (myname,mysoname,dateof) VALUES (%s,%s,%s);""",(soname, name, birthday))
        print("[INFO] Data was successfully inserted")
        self.__connection.commit
        #cursor.close()
        #self.__connection.close()
        # print("[INFO] PostgreSQL connection closed")

    def list_messages(self, soname: str, name: str): # получение данных
        conn = self.__connection  # СОЗДАНИЕ ПОДКЛЮЧЕНИЯ
        cursor = conn.cursor()  # СОЗДАНИЕ ПАЧКИ ЗАПРОСОВ ДЛЯ ОТПРАВКИ В БД
        cursor.execute("""SELECT dateof FROM birthday WHERE mysoname='Прокофьев' AND myname='Михаил';""")

        return cursor.fetchone()
        self.__connection.commit
        #print(str(blood))
        #cursor.close()
        #self.__connection.close()
        # print("[INFO] PostgreSQL connection closed")

    def result(self, mysoname: str, myname: str):
        r = self.list_messages(mysoname, myname)
        print(r)

    def kolvo(self,birthday):
        kol = 0
        for bigb in birthday:
            kol += 1
        if kol < 5:
            print('ОШИБКА!!!')
            print('Введите дату своего рождения в формате: ДД-ММ')
            birthday = input()
            self.kolvo(birthday)

    def cikl(self,birthday):
        i = -1
        for letter in birthday:
            i += 1
            if letter == '0' and i == 0 or letter == '1' and i == 0 or letter == '2' and i == 0 or letter == '3' and i == 0:
                pass
            elif letter == '0' and i == 1 or letter == '1' and i == 1 or letter == '2' and i == 1 or letter == '3' and i == 1 or letter == '4' and i == 1 or letter == '5' and i == 1 or letter == '6' and i == 1 or letter == '7' and i == 1 or letter == '8' and i == 1 or letter == '9' and i == 1:
                pass
            elif letter == '-' and i == 2:
                pass
            elif letter == '0' and i == 3 or letter == '1' and i == 3:
                pass
            elif letter == '0' and i == 4 or letter == '1' and i == 4 or letter == '2' and i == 4 or letter == '3' and i == 4 or letter == '4' and i == 4 or letter == '5' and i == 4 or letter == '6' and i == 4 or letter == '7' and i == 4 or letter == '8' and i == 4 or letter == '9' and i == 4:
                pass
            else:
                print('ОШИБКА!!!')
                print('Введите дату своего рождения повторно в формате: ДД-ММ')
                birthday = input()
                self.cikl(birthday)

currency=Super()
print('Введите свое имя:')
name=input()
print('Введите свою фамилию:')
soname=input()
print('Введите дату своего рождения в формате: ДД-ММ')
birthday=input()
currency.kolvo(birthday)
currency.cikl(birthday)
currency.init_db()
currency.add_message(soname,name,birthday)
currency.result(soname,name)
currency.chech_currency()
