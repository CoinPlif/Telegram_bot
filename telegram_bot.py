import telebot
import sqlite3
from aiogram import types
from aiogram.utils.markdown import hlink
from telebot import types
admin_id=1025201891

bot = telebot.TeleBot('2013284515:AAFuv4gYjYqz4S7FfxDTU5EhNZgtZfXD3nY')

@bot.message_handler(commands=['start'])
def start(message):
    #bot.send_message(message.chat.id, 'Привет! ' + "Итак я умею:" + "\n" + "/start - старт бота" + "\n" + "/form - заполнить анкету" + "\n"
    #                 + "/form_customer - посмотреть свою анкету заказчика" + "\n" + "/form_freelancer - посмотреть свою анкету фрилансера" + "\n" + "/delete_customers - удалиться из заказчиков"
    #                 + "\n" + "/delete_freelancers - удалиться из заказчиков" + "\n" + "/change_customer_form - изменить анкету заказчика" + "\n" + "/change_freelancer_form - изменить анкету фрилансера"
    #                 + "\n" + "/search_customer - найти заказчика" + "\n" + "/search_freelancer - найти фрилансера" + "")
    bot.send_message(message.chat.id, text = hlink("Договор оферта", "https://docs.google.com/document/d/1NjDw6zkHr-tCKvxdJF-aynmBk_qwEFasZ8Btwyw5vOU/edit"), parse_mode="HTML")
    bot.register_next_step_handler(message, start_DB_oferta)
    soglasie(message)
@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,
                     'Привет! ' + "Итак я умею:"  + "\n" + "/form - заполнить анкету" + "\n"
                     + "/form_customer - посмотреть свою анкету заказчика" + "\n" + "/form_freelancer - посмотреть свою анкету фрилансера" + "\n" + "/delete_customers - удалиться из заказчиков"
                     + "\n" + "/delete_freelancers - удалиться из заказчиков" + "\n" + "/change_customer_form - изменить анкету заказчика" + "\n" + "/change_freelancer_form - изменить анкету фрилансера"
                     + "\n" + "/search_customer - найти заказчика" + "\n" + "/search_freelancer - найти фрилансера" + "")
def soglasie(message):
    sogl=bot.send_message(message.chat.id, "Внимательно прочитайте и согласитесь с договором офера(напишите да(если согласны)/нет(если не согласны))")
    bot.register_next_step_handler(sogl, soglasie_s_oferta)
def soglasie_s_oferta(message):
    print(message.text)
    if "да" in message.text:
        connect = sqlite3.connect('dostup.db')
        cursor = connect.cursor()
        sql_update = """UPDATE Users set agree_oferta = ? WHERE id = ?"""
        cursor.execute(sql_update, (1, message.chat.id))
        connect.commit()
        bot.send_message(message.chat.id, "Вы согласились с договором оферта!" + "\n" + "Теперь перейдем к оплате")
        print('re')
        plata(message)
    else:
        bot.send_message(message.chat.id, "Вы не согласились с договором оферта, отказанно в доступе использования бота")
def plata(message):
    bot.send_message(message.chat.id, "Для того, чтобы оставить свою заявку фрилансера/заказчика вам нужно:"+"\n" +"1)переведите 50 рублей по номеру телефона 89851671967 с сообщением \"sdvig\""+"\n"+
                     "после оплаты отправьте скриншот перевода https://vk.com/coinlord и в течение 5 минут бот сообщит об открытии доступа к его функционалу")
    bot.send_message(admin_id, f"чел с id={message.chat.id} перешел к оплате")

def start_DB_oferta(message):
    connect = sqlite3.connect('dostup.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INT,
        agree_oferta INT,
        agree_plata INT
    )""")
    connect.commit()
    Customers_id = message.chat.id
    cursor.execute(f"SELECT id FROM Users WHERE id = {Customers_id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO Users VALUES('{Customers_id}','{0}','{0}')")
        connect.commit()
@bot.message_handler(commands=['add'])
def add(message):
    chel_id = bot.send_message(admin_id, "введите id пользователя, которого хотите добавить:")
    bot.register_next_step_handler(message,add_to)

def add_to(message):
    chel_id = message.text
    print(message.text)
    add_to_db(chel_id)


def add_to_db(chel_id):
    connect = sqlite3.connect('dostup.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Users set agree_plata = ? WHERE id = ?"""
    cursor.execute(sql_update, (1, chel_id))
    connect.commit()
    bot.send_message(admin_id, f"Вы разрешили пользователю с id={chel_id} пользоваться вашим ботом")
    bot.send_message(chel_id, "Теперь вы можете пользоваться ботом")

def delete_сustomers(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    Customers_id = message.chat.id
    cursor.execute(f"DELETE FROM Customers WHERE id = {Customers_id}")
    connect.commit()
    bot.send_message(message.chat.id, "Вы удалили анкету заказчика")

def delete_freelancers(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    Freelancer_id = message.chat.id
    cursor.execute(f"DELETE FROM Freelancers WHERE id = {Freelancer_id}")
    connect.commit()
    bot.send_message(message.chat.id, "Вы удалили анкету фрилансера")

@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text.lower() == "/form":
        form(message)
    elif  message.text.lower() == "/form_customer":
        form_customer(message)
    elif  message.text.lower() == "/form_freelancer":
        form_freelancer(message)
    elif message.text.lower() == "/delete_customers":
        delete_сustomers(message)
    elif message.text.lower() == "/delete_freelancers":
        delete_freelancers(message)
    elif message.text.lower() == "/change_freelancer_form":
        changes_freelancer_form(message)
    elif message.text.lower() == "/change_customer_form":
        change_customer_form(message)
    elif message.text.lower() == '/search_customer':
        search_customer(message)
    elif message.text.lower() == '/search_freelancer':
        search_freelancer(message)
    else:
        comands=bot.send_message(message.chat.id, 'Я не знаю такой команды...')
        bot.register_next_step_handler(comands, commands)

def search_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sqlite_select_query = """SELECT Freelancer_occupation FROM Freelancers where id =?"""
    cursor.execute(sqlite_select_query, (message.chat.id,))
    freelancers = cursor.fetchone()
    request = freelancers[0]
    y = cursor.execute("""SELECT * FROM Customers""").fetchall()
    for row in y:
        if request in row[4]:
            bot.send_message(message.chat.id, "Имя фамилия: " + row[1] + " " + row[2] + "\n" + "Название компании: " + row[3] + "\n" + "Род деятельности фрилансера, которого хотят нанять: " + row[4] + "\n" + "Телефон: " + row[5])

def search_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sqlite_select_query = """SELECT Customer_occupation FROM Customers where id =?"""
    cursor.execute(sqlite_select_query, (message.chat.id,))
    customers = cursor.fetchone()
    request = customers[0]
    jobs = request.split(",")
    print(jobs[0])
    y = cursor.execute("""SELECT * FROM Freelancers""").fetchall()
    for i in range(len(jobs)):
        for row in y:
            print(jobs, i)
            if jobs[i] in row[3]:
                bot.send_message(message.chat.id, "Имя фамилия: " + row[1] + " " + row[2] + "\n" + "Род деятельности: " + row[3] + "\n" + "Телефон: " + row[4])

def start_DB_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Customers(
        id INT,
        Customer_name TEXT,
        Customer_sname TEXT,
        Customer_name_of_company TEXT,
        Customer_occupation TEXT,
        Customer_telephone TEXT
    )""")
    connect.commit()
    Customers_id = message.chat.id
    cursor.execute(f"SELECT id FROM Customers WHERE id = {Customers_id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO Customers VALUES('{Customers_id}', '{NAME}', '{SNAME}', '{COMPANY_NAME}', '{OCCUPATION}', '{TELEPHONE}')")
        connect.commit()
        bot.send_message(message.chat.id, "Зарегистрировались!" + '\n' + 'Нажмите /search_freelancer для того чтобы найти фрилансера по вашей специализации')
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!" + '\n' + "Нажмите /search_freelancer для того чтобы найти фрилансера по вашей специализации")

def start_DB_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Freelancers(
        id INT,
        Freelancer_name TEXT,
        Freelancer_sname TEXT,
        Freelancer_occupation TEXT,
        Freelancer_telephone TEXT
    )""")
    connect.commit()
    Freelancer_id = message.chat.id
    cursor.execute(f"SELECT id FROM Freelancers WHERE id = {Freelancer_id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO Freelancers VALUES('{Freelancer_id}', '{NAME}', '{SNAME}', '{OCCUPATION}', '{TELEPHONE}')")
        connect.commit()
        bot.send_message(message.chat.id, "Зарегистрировались!" + '\n' + '/search_customer для того чтобы найти заказчика по вашей специализации')
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!" + '\n' + "Нажмите /search_customer для того чтобы найти заказчика по вашей специализации")


def form_customer(message):
    Availability = 0
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    person_id = message.chat.id
    cursor.execute("""SELECT * from Customers """)
    records = cursor.fetchall()
    for row in records:
        if row[0] == person_id:
            Availability = 1
            break
    if Availability == 1:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        person_id = message.chat.id
        cursor.execute("""SELECT * from Customers where id = ?""", (person_id,))
        row = cursor.fetchone()
        bot.send_message(message.chat.id, "Ваша анкета заказчика: " + "\n\n" + "Имя: " + row[1] + "\n" + "Фамилия: " + row[2] + "\n" + "Название компании: " + row[3] + "\n" + "Род деятельности фрилансера, которого хотите нанять: " + row[4] + "\n" + "Номер телефона: " + row[5])
    else:
        bot.send_message(message.chat.id, "У вас еще нет анкеты заказчика" + "\n" + "Чтобы создать анкету используйте команду /form")

def form_freelancer(message):
    Availability = 0
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    person_id = message.chat.id
    cursor.execute("""SELECT * from Freelancers """)
    records = cursor.fetchall()
    for row in records:
        if row[0] == person_id:
            Availability = 1
            break
    if Availability == 1:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        person_id = message.chat.id
        cursor.execute("""SELECT * from Freelancers where id = ?""", (person_id,))
        row = cursor.fetchone()
        bot.send_message(message.chat.id, "Ваша анкета фрилансера: " + "\n\n" + "Имя: " + row[1] + "\n" + "Фамилия: " + row[2] + "\n" + "Род деятельности: " + row[3] + "\n" + "Номер телефона: " + row[4])
    else:
        bot.send_message(message.chat.id, "У вас еще нет анкеты фрилансера" + "\n" + "Чтобы создать анкету используйте команду /form")

def form(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Заказчик', callback_data='заказчик')
    item1 = types.InlineKeyboardButton('Фрилансер', callback_data='фрилансер')
    markup.add(item, item1)
    bot.send_message(message.chat.id, "Кто ты, заказчик или фрилансер? ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - заказчик')
            name_customer(identity)
        elif call.data == 'фрилансер':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - фрилансер')
            name_freelancer(identity)
        elif call.data == 'Имя_фрилансер':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить имя')
            change_name_freelancer_before(identity)
        elif call.data == 'Фамилия_фрилансер':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить фамилию')
            change_sname_freelancer_before(identity)
        elif call.data == 'Род_деятельности_фрилансер':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить род деятельности')
            change_occupation_freelancer_before(identity)
        elif call.data == 'Номер_телефона_фрилансер':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить номер телефона')
            change_telephone_freelancer_before(identity)
        elif call.data == 'Имя_заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить имя')
            change_name_customer_before(identity)
        elif call.data == 'Фамилия_заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить фамилию')
            change_sname_customer_before(identity)
        elif call.data == 'Название_компании_заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить название компании')
            change_name_of_company_customer_before(identity)
        elif call.data == 'Род_деятельности_заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить род деятельности')
            change_occupation_customer_before(identity)
        elif call.data == 'Номер_телефона_заказчик':
            identity = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Вы выбрали - изменить номер телефона')
            change_telephone_customer_before(identity)

def name_customer(message):
    names = bot.send_message(message.chat.id, "Теперь давай узнаем некоторую нужную информацию о тебе."+"\n"+"Введите полное имя: ")
    bot.register_next_step_handler(names, surename_customer)

def surename_customer(message):
    surenames = bot.send_message(message.chat.id, "Введите полную фамилию: ")
    bot.register_next_step_handler(surenames, user_name_of_company_customer)
    global NAME
    NAME = message.text

def user_name_of_company_customer(message):
    user_names_of_company = bot.send_message(message.chat.id, "Введите название компании: ")
    bot.register_next_step_handler(user_names_of_company, occupations_customer)
    global SNAME
    SNAME = message.text

def occupations_customer(message):
    occupations_s = bot.send_message(message.chat.id, "Введите род деятельности фрилансера, которого хотите нанять(через запятую): ")
    bot.register_next_step_handler(occupations_s, telephone_customer)
    global COMPANY_NAME
    COMPANY_NAME = message.text

def telephone_customer(message):
    occupations_s = bot.send_message(message.chat.id, "Введите ваш номер телефона: ")
    bot.register_next_step_handler(occupations_s, dopchik_customer)
    global OCCUPATION
    OCCUPATION = message.text

def dopchik_customer(message):
    global TELEPHONE
    TELEPHONE = message.text
    start_DB_customer(message)

def name_freelancer(message):
    names = bot.send_message(message.chat.id, "Введите полное имя: ")
    bot.register_next_step_handler(names, surename_freelancer)

def surename_freelancer(message):
    surenames = bot.send_message(message.chat.id, "Введите полную фамилию: ")
    bot.register_next_step_handler(surenames, user_occupations_freelancer)
    global NAME
    NAME = message.text

def user_occupations_freelancer(message):
    occupations = bot.send_message(message.chat.id, "Введите род деятельности: ")
    bot.register_next_step_handler(occupations, telephone_freelancer)
    global SNAME
    SNAME = message.text

def telephone_freelancer(message):
    occupations = bot.send_message(message.chat.id, "Введите ваш номер телефона: ")
    bot.register_next_step_handler(occupations, dopchik_freelancer)
    global OCCUPATION
    OCCUPATION = message.text

def dopchik_freelancer(message):
    global TELEPHONE
    TELEPHONE = message.text
    start_DB_freelancer(message)

def changes_freelancer_form(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Имя', callback_data='Имя_фрилансер')
    item1 = types.InlineKeyboardButton('Фамилия', callback_data='Фамилия_фрилансер')
    item2 = types.InlineKeyboardButton('Род деятельности', callback_data='Род_деятельности_фрилансер')
    item3 = types.InlineKeyboardButton('Номер телефона', callback_data='Номер_телефона_фрилансер')
    markup.add(item, item1, item2, item3)
    bot.send_message(message.chat.id, "Что изменяем? ", reply_markup=markup)

def change_name_freelancer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененное имя: ")
    bot.register_next_step_handler(names, change_name_freelancer)

def change_name_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Freelancers set Freelancer_name = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Имя изменено!")

def change_sname_freelancer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененную фамилию: ")
    bot.register_next_step_handler(names, change_sname_freelancer)

def change_sname_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Freelancers set Freelancer_sname = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Фамилия изменено!")

def change_occupation_freelancer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененный род деятельности: ")
    bot.register_next_step_handler(names, change_occupation_freelancer)

def change_occupation_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Freelancers set Freelancer_occupation = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Род деятельности изменён!")

def change_telephone_freelancer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененный номер телефона: ")
    bot.register_next_step_handler(names, change_telephone_freelancer)

def change_telephone_freelancer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Freelancers set Freelancer_telephone = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Номер телефона изменён!")

def change_customer_form(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Имя', callback_data='Имя_заказчик')
    item1 = types.InlineKeyboardButton('Фамилия', callback_data='Фамилия_заказчик')
    item2 = types.InlineKeyboardButton('Название компании', callback_data='Название_компании_заказчик')
    item3 = types.InlineKeyboardButton('Род деятельности', callback_data='Род_деятельности_заказчик')
    item4 = types.InlineKeyboardButton('Номер телефона', callback_data='Номер_телефона_заказчик')
    markup.add(item, item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Что изменяем? ", reply_markup=markup)

def change_name_customer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененное имя: ")
    bot.register_next_step_handler(names, change_name_customer)

def change_name_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Customers set Customer_name = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Имя изменено!")

def change_sname_customer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененную фамилию: ")
    bot.register_next_step_handler(names, change_sname_customer)

def change_sname_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Customers set Customer_sname = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Фамилия изменено!")

def change_name_of_company_customer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененное название компании: ")
    bot.register_next_step_handler(names, change_name_of_company_customer)

def change_name_of_company_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Customers set Customer_name_of_company = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Название компании изменена!")

def change_occupation_customer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененный род деятельности: ")
    bot.register_next_step_handler(names, change_occupation_customer)

def change_occupation_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Customers set Customer_occupation = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Род деятельности изменен!")

def change_telephone_customer_before(message):
    names = bot.send_message(message.chat.id, "Введите измененный номер телефона: ")
    bot.register_next_step_handler(names, change_telephone_customer)

def change_telephone_customer(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sql_update = """UPDATE Customers set Customer_telephone = ? WHERE id = ?"""
    cursor.execute(sql_update, (message.text, message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Номер телефона изменён!")
bot.polling(none_stop=True, interval=0)




