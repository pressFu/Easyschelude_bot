import telebot
from telebot import types
import datetime


bot = telebot.TeleBot('5781286264:AAGUHHvxzvBzefuwafVmS0XkuAtCzSWPTYs')


def define_week():
    """
    Функция, которая возвращает четность недели
    True: Возвращает нечетную неделю
    False: Возвращает четную неделю

    Attributes:
        now_date: сегодняшняя дата
        start_date: дата откуда начинает вестись счет
        quantity_day: разница дней от начального до настоящего
        counter_week: количество недель

    :return: True or False
    """
    now_date = datetime.datetime.now()
    start_date = datetime.datetime(2022, 9, 1)
    quantity_day = now_date - start_date
    days = quantity_day.days
    counter_week = 0
    for i_day in range(quantity_day.days):
        days -= 7
        counter_week += 1
    if counter_week % 2 == 0:
        return True
    else:
        return False


def get_schedule(message, day=0):
    """
    Функция печатающая сообщение в боте

    Attributes:
        lessons: сюда записываются предметы
        today: переменная хранит в себе значение дня

    :param message: передается чат
    :param day: передается день недели
    """
    lessons = ''
    today = message.text

    if day == 0:
        pass
    elif day == 1:
        today = 'Понедельник'
    elif day == 2:
        today = 'Вторник'
    elif day == 3:
        today = 'Среда'
    elif day == 4:
        today = 'Четверг'
    elif day == 5:
        today = 'Пятница'
    elif day == 6:
        today = 'Суббота'

    if define_week():
        for i_item in range(len(schedule_even.get(today))):
            lessons += schedule_even[today][i_item] + '\n'
    else:
        for i_item in range(len(schedule_not_even.get(today))):
            lessons += schedule_not_even[today][i_item] + '\n'
    bot.send_message(message.chat.id, lessons)


schedule_even = {'Понедельник': ['11:40 Рекламист', '13:45 Рекламист'],
                 'Вторник': ['8:00 Коновалов', '9:50 Коновалов'],
                 'Среда': ['9:50 Английский'],
                 'Четверг': ['8:00 Аникина', '9:50 Карев', '11:40 Гилева'],
                 'Пятница': ['11:40 Карев', '13:45 Английский', '15:35 Аникина'],
                 'Суббота': ['3 пары Моны']}

schedule_not_even = {'Понедельник': ['11:40 Рекламист', '13:45 Рекламист'],
                 'Вторник': ['8:00 Аникина', '9:50 Коновалов'],
                 'Среда': ['9:50 Английский'],
                 'Четверг': ['8:00 Гилева', '9:50 Карев', '11:40 Гилева'],
                 'Пятница': ['Нет пар'],
                 'Суббота': ['3 пары Моны']}


@bot.message_handler(commands=['start'])
def start(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание на сегодня')
    btn2 = types.KeyboardButton('Другой день')
    markup_menu.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет, я помогу тебе с расписанием =)', reply_markup=markup_menu)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сегодня 📃')
    btn2 = types.KeyboardButton('Другой день 🎓')
    markup_menu.add(btn1, btn2)
    if message.text == 'Сегодня 📃':
        now_date = datetime.date.today()    # Получаю текущую дату
        print_date = str(now_date)      # Преобразую дату в str для отправки сообщения
        bot.send_message(message.chat.id, 'Твое расписание на {date}'.format(date=print_date))
        if define_week():
            bot.send_message(message.chat.id, 'Четная неделя')
        else:
            bot.send_message(message.chat.id, 'Нечетная неделя')
        number_day = datetime.datetime.today().weekday()
        get_schedule(message, day=number_day)
    elif message.text == 'Другой день 🎓':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Понедельник')
        button2 = types.KeyboardButton('Вторник')
        button3 = types.KeyboardButton('Среда')
        button4 = types.KeyboardButton('Четверг')
        button5 = types.KeyboardButton('Пятница')
        button6 = types.KeyboardButton('Суббота')
        button7 = types.KeyboardButton('Меню')
        markup.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, 'Какой день на этой неделе?', reply_markup=markup)

    elif message.text == 'Меню':
        bot.send_message(message.chat.id, 'Вы вернулись в меню', reply_markup=markup_menu)

    elif message.text == 'Понедельник':
        get_schedule(message)

    elif message.text == 'Вторник':
        get_schedule(message)

    elif message.text == 'Среда':
        get_schedule(message)

    elif message.text == 'Четверг':
        get_schedule(message)

    elif message.text == 'Пятница':
        get_schedule(message)

    elif message.text == 'Суббота':
        get_schedule(message)

    else:
        bot.send_message(message.chat.id, 'Не знаю что делать =(')


bot.polling(none_stop=True, interval=0)
