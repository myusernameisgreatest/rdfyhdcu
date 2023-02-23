import requests
from bs4 import BeautifulSoup
import time
import random
import datetime
import psycopg2
from conf import host, user, password, db_name


class Super:
    sayt = 'https://www.google.ru/search?q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B2+%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B7%D0%BD%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%B5&newwindow=1&sxsrf=AJOqlzUYMY_AXixbjGjIsYJwKEyktMDX0Q%3A1676367414314&ei=NlbrY6fjEvKGwPAP5o-P2AE&ved=0ahUKEwin1vih25T9AhVyAxAIHebHAxsQ4dUDCBA&uact=5&oq=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B2+%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B7%D0%BD%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%B5&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIMCAAQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyEgguEMcBENEDEOoCELQCEEMYATIMCAAQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyEgguEMcBENEDEOoCELQCEEMYATISCC4QxwEQ0QMQ6gIQtAIQQxgBMgwIABDqAhC0AhBDGAEyDAgAEOoCELQCEEMYATIMCAAQ6gIQtAIQQxgBSgQIQRgASgQIRhgBUABYqjxgv0BoAXABeACAAQCIAQCSAQCYAQCgAQGwARTAAQHaAQYIARABGAE&sclient=gws-wiz-serp'
    # google
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    # what i'm not bot
    current_converted_price = 0 # for temperature
    difference = 1  # difference of temperature
    pozdr = 0  # for one congratulation
    denr = 0  # for one congratulation birthday
    name = 'имя'
    soname = 'фамилия'
    birthday = '07-01'
    __connection = None

    def get_currency_price(self):  # get temperature from google
        full_page = requests.get(self.sayt, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "wob_t", "class": "q8U8x"})  # from string in console from browser
        return convert[0].text

    def chech_currency(self):  # for print random text in subject when temperature different from previous value
        currency = int(self.get_currency_price())  # how __init__!
        if currency >= self.current_converted_price + self.difference:
            m = random.randrange(0, 3, 1)
            if m == 0:
                print("Потеплело, снимай шапку!")
            if m == 1:
                print("Потеплело, снимай куртку!")
            if m == 2:
                print("Потеплело, снимай перчатки!")
            self.current_converted_price = currency
        elif currency <= self.current_converted_price - self.difference:
            m = random.randrange(0, 10, 1)
            if m == 0:
                print("Похолодало, надевай шапку!")
            if m == 1:
                print("Похолодало, надевай куртку!")
            if m == 2:
                print("Похолодало, надевай перчатки!")
            self.current_converted_price = currency  # update the last temperature value
        now = datetime.datetime.now()  # create current time
        print(now.strftime("%d-%m-%Y %H:%M"))
        data = now.strftime("%d-%m")  # for input birthday
        with self.__connection as connection:
            with connection.cursor() as cursor:
                # checking if today is a holiday
                cursor.execute("""SELECT name FROM holidays WHERE  dat=%s;""", (data, ))
                prazdnik = cursor.fetchone()
        if prazdnik[0] == None:
            pass
        elif self.pozdr == 0:
            print('С праздником: '+prazdnik[0]+'!!!')
            self.pozdr = 1  # for don't repeat

        if data == birthday and self.denr == 1:  # checking if today is a birthday of user
            print('С днем рождения, '+name+' '+soname+'!!!')
            self.denr = 1  # for don't repeat
        print('Температура воздуха в Краснознаменске сейчас '+str(currency)+' оС')
        time.sleep(300)
        self.chech_currency()  # repeat

    def init_db(self):  # checking the existence of the desired table, otherwise - creating
        # connection.autocommit = True
        if self.__connection is None:
            self.__connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with self.__connection as connection:
            with connection.cursor() as cursor:

                cursor.execute("""CREATE TABLE IF NOT EXISTS birthday(
                            id          serial PRIMARY KEY,
                            myname      varchar NOT NULL,
                            mysoname    varchar NOT NULL,
                            dateof      varchar NOT NULL);""")
                connection.commit  # not needed?

    def add_message(self, soname: str, name: str, birthday: str):  # add data about user
        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO birthday (myname, mysoname, dateof) VALUES (%s,%s,%s);""",
                               (name, soname, birthday))
                connection.commit  # not needed?
                print("[INFO] Data was successfully inserted")

    def list_messages(self, soname: str, name: str):  # get data about birthday of user
        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT dateof FROM birthday WHERE mysoname=%s AND myname=%s ORDER BY myname;""", (soname, name))
                data_birth = cursor.fetchone()
                print('Ты родился: ', data_birth[0])  # to show the user that he is already registered
                return cursor.fetchone()
                cursor.close()  # not needed?
                self.__connection.close()  # and this needed?
                print("[INFO] PostgreSQL connection closed")

    def proverka_nalichia(self, soname: str, name: str):  # check data of user in db
        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT dateof FROM birthday WHERE mysoname=%s AND myname=%s ORDER BY myname;""", (soname, name))
                return cursor.fetchone()

    def kolvo(self, birthday):  # character count check for birthday
        if len(birthday) < 5 or len(birthday) > 5:
            print('ОШИБКА!!!')
            print('Введите дату своего рождения в формате: ДД-ММ')
            birthday = input()
            self.kolvo(birthday)

    def cikl(self, birthday):  # format conformance check for birthday
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


currency = Super()
print('Введите свое имя:')
name = input()
print('Введите свою фамилию:')
soname = input()
currency.init_db()
if currency.proverka_nalichia(soname, name) == None:  # for new user
    print('Введите дату своего рождения в формате: ДД-ММ')
    birthday = input()
    currency.kolvo(birthday)
    currency.cikl(birthday)
    currency.add_message(soname, name, birthday)
else:
    birthday = currency.list_messages(soname, name)
currency.chech_currency()
