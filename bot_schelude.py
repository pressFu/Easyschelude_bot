"""
Этот бот написан @kissordead
Version 1.3

Бот создан для упрощения поиска расписания
"""


import telebot
from telebot import types
import datetime
import time

bot = telebot.TeleBot('5781286264:AAGUHHvxzvBzefuwafVmS0XkuAtCzSWPTYs')


class Human:
    """
    Базовый класс Человек
    """
    request_week = dict()
    id_human = None


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
    start_date = datetime.datetime(2022, 8, 29)
    quantity_day = now_date - start_date
    days = quantity_day.days
    week = 7
    counter_week = 0
    while week < days:
        days -= week
    if counter_week % 2 == 0:
        return False
    else:
        return True


def get_schedule(message, markup, day=0, even=False, not_even=False):
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

    if even:
        for i_item in range(len(schedule_even.get(today))):
            lessons += schedule_even[today][i_item] + '\n'
    elif not_even:
        for i_item in range(len(schedule_not_even.get(today))):
            lessons += schedule_not_even[today][i_item] + '\n'
    elif define_week():
        for i_item in range(len(schedule_even.get(today))):
            lessons += schedule_even[today][i_item] + '\n'
    elif not define_week():
        for i_item in range(len(schedule_not_even.get(today))):
            lessons += schedule_not_even[today][i_item] + '\n'
    bot.send_message(message.chat.id, lessons, reply_markup=markup)


def print_even_week(message):
    """
    Функция отправляющая четность недели

    :param message: отправляется принятое сообщение

    :return: четность в виде ответа сообщением
    """
    if define_week():
        bot.send_message(message.chat.id, 'Четная неделя')
    else:
        bot.send_message(message.chat.id, 'Нечетная неделя')


def menu_marcup():
    """
    Функция кнопок меню

    :return: marcup_menu
    """
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сегодня 📃')
    btn2 = types.KeyboardButton('Завтра')
    btn3 = types.KeyboardButton('Другой день 🎓')
    markup_menu.add(btn1, btn2, btn3)
    return markup_menu


def even_not_even():
    markup_week = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_even = types.KeyboardButton('Четная')
    button_not_even = types.KeyboardButton('Нечетная')
    button_menu = types.KeyboardButton('Меню')
    markup_week.add(button_even, button_not_even, button_menu)
    return markup_week


def markup_day():
    markup_days = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Понедельник')
    button2 = types.KeyboardButton('Вторник')
    button3 = types.KeyboardButton('Среда')
    button4 = types.KeyboardButton('Четверг')
    button5 = types.KeyboardButton('Пятница')
    button6 = types.KeyboardButton('Суббота')
    button7 = types.KeyboardButton('Меню')
    markup_days.add(button1, button2, button3, button4, button5, button6, button7)
    return markup_days


def read_action(message, human):
    if message.text == 'Сегодня 📃':
        now_date = datetime.date.today()  # Получаю текущую дату
        print_date = str(now_date)  # Преобразую дату в str для отправки сообщения
        bot.send_message(message.chat.id, 'Твое расписание на {date}'.format(date=print_date))
        print_even_week(message)
        number_day = datetime.datetime.today().weekday() + 1
        get_schedule(message, 0, day=number_day)

    elif message.text == 'Завтра':
        """
        Проверка Завтра

        Attributes:
            number_day: номер следующего дня

        Work:
            Если следующий день воскресенье, печатаем
            Иначе, если номер следующего дня на следующей неделе, то проверяем четность и
            выводим расписание на следующий день с последующей четностью недели
        """
        number_day = datetime.datetime.today().weekday() + 2
        if number_day == 7:
            bot.send_message(message.chat.id, 'В воскресенье отдыхаем, расслабься)', reply_markup=menu_marcup())
        elif number_day == 8:   # Понедельник следующей недели
            if define_week():  # Возвращает True (Нечетная неделя)
                get_schedule(message, 0, day=1)
            else:
                get_schedule(message, 0, day=1)
        else:  # Если завтрашний день от пн до сб, выводим расписание следующего дня
            get_schedule(message, 0, day=number_day)

    elif message.text == 'Другой день 🎓':
        print_even_week(message)  # Выводим какая сейчас неделя, чтобы было проще ориентироваться в выборе
        bot.send_message(message.chat.id, 'Какую неделю смотрим?', reply_markup=even_not_even())

    elif message.text == 'Четная':
        human.request_week[human.id_human] = 'Четная'
        bot.send_message(message.chat.id, 'Какой день на этой неделе?', reply_markup=markup_day())

    elif message.text == 'Нечетная':
        human.request_week[human.id_human] = 'Нечетная'
        bot.send_message(message.chat.id, 'Какой день на этой неделе?', reply_markup=markup_day())

    elif message.text == 'Меню':
        if human.request_week.get(message.chat.id):
            human.request_week.pop(message.chat.id)
        bot.send_message(message.chat.id, 'Вы вернулись в меню', reply_markup=menu_marcup())

    elif message.text == 'Понедельник':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())

    elif message.text == 'Вторник':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())

    elif message.text == 'Среда':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())
    elif message.text == 'Четверг':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())

    elif message.text == 'Пятница':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())

    elif message.text == 'Суббота':
        if human.request_week.get(human.id_human) == 'Четная':
            get_schedule(message=message, markup=markup_day(), even=True)
        elif human.request_week.get(human.id_human) == 'Нечетная':
            get_schedule(message=message, markup=markup_day(), not_even=True)
        else:
            get_schedule(message, markup=menu_marcup())
    else:
        bot.send_message(message.chat.id, 'Не знаю что делать =(')


schedule_even = {'Понедельник': ['Нет пар'],
                 'Вторник': ['8:00 Коновалов 364 к5', '9:50 Коновалов 407 к1'],
                 'Среда': ['9:50 Английский к5'],
                 'Четверг': ['8:00 Аникина 415 к1', '9:50 Карев 422 к1', '11:40 Гилева 234 к5'],
                 'Пятница': ['11:40 Карев 228 к5', '13:45 Английский к5', '15:35 Аникина 452 к5'],
                 'Суббота': ['11:40 Кулаковский 452 к5']}

schedule_not_even = {'Понедельник': ['11:40 Рекламист 333к', '13:45 Рекламист 333к'],
                     'Вторник': ['8:00 Аникина 219 к5', '9:50 Коновалов 364 к5'],
                     'Среда': ['9:50 Английский к5'],
                     'Четверг': ['8:00 Гилева 422 к1', '9:50 Карев 422 к1', '11:40 Гилева 452 к5'],
                     'Пятница': ['Нет пар'],
                     'Суббота': ['11:40 Кулаковский 452 к5']}


human = Human()
human_ID = 100_000


try:
    @bot.message_handler(commands=['start'])
    def start(message):
        # human.id_human = message.chat.id
        bot.send_message(message.chat.id, 'Привет, я помогу тебе с расписанием!', reply_markup=menu_marcup())


    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        """    Функция принимающая сообщение   """
        human.id_human = message.chat.id
        read_action(message, human=human)
        print(human.request_week)


    bot.polling(none_stop=True)


except Exception:
    bot.polling(none_stop=True)
