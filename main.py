"""
Этот бот написан @kissordead
Version 1.2

Бот создан для упрощения поиска расписания
"""

# Хочу сделать кнопку выбора четности недели перед выбором дня для которого нужно расписание

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


def get_schedule(message, day=0, even=False, not_even=False):
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

    if define_week() or even:
        for i_item in range(len(schedule_even.get(today))):
            lessons += schedule_even[today][i_item] + '\n'
    elif not define_week() or not_even:
        for i_item in range(len(schedule_not_even.get(today))):
            lessons += schedule_not_even[today][i_item] + '\n'
    bot.send_message(message.chat.id, lessons)


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


schedule_even = {'Понедельник': ['11:40 Рекламист 333 к5', '13:45 Рекламист 333 к5'],
                 'Вторник': ['8:00 Коновалов 364 к5', '9:50 Коновалов 407 к1'],
                 'Среда': ['9:50 Английский к5'],
                 'Четверг': ['8:00 Аникина 415 к1', '9:50 Карев 422 к1', '11:40 Гилева 234 к5'],
                 'Пятница': ['11:40 Карев 228 к5', '13:45 Английский к5', '15:35 Аникина 452 к5'],
                 'Суббота': ['3 пары Моны к5']}

schedule_not_even = {'Понедельник': ['11:40 Рекламист 333к', '13:45 Рекламист 333к'],
                 'Вторник': ['8:00 Аникина 219 к5', '9:50 Коновалов 364 к5'],
                 'Среда': ['9:50 Английский к5'],
                 'Четверг': ['8:00 Гилева 422 к1', '9:50 Карев 422 к1', '11:40 Гилева 452 к5'],
                 'Пятница': ['Нет пар'],
                 'Суббота': ['3 пары Моны к5']}


@bot.message_handler(commands=['start'])
def start(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сегодня 📃')
    btn2 = types.KeyboardButton('Другой день 🎓')
    markup_menu.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет, я помогу тебе с расписанием =)', reply_markup=markup_menu)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Функция читающая бота

    Args:
        message: принимает сообщение

    Attributes:
        markup_menu): набор кнопок в главном меню
        markup: набор кнопок с днями недели, включая выход в меню
        btn1,2,3: кнопки меню
        now_date (date): актуальная дата
        number_day (int): принимает значение нужного дня
    """
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сегодня 📃')
    btn2 = types.KeyboardButton('Завтра')
    btn3 = types.KeyboardButton('Другой день 🎓')
    markup_menu.add(btn1, btn2, btn3)

    if message.text == 'Сегодня 📃':
        now_date = datetime.date.today()    # Получаю текущую дату
        print_date = str(now_date)      # Преобразую дату в str для отправки сообщения
        bot.send_message(message.chat.id, 'Твое расписание на {date}'.format(date=print_date))
        print_even_week(message)
        number_day = datetime.datetime.today().weekday() + 1
        get_schedule(message, day=number_day)

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
            bot.send_message(message.chat.id, 'В воскресенье отдыхаем, расслабься)', reply_markup=markup_menu)
        elif number_day > 7:
            number_day %= 7
            if define_week():   # Возвращает True (Нечетная неделя)
                get_schedule(message, number_day, even=True)
            else:
                get_schedule(message, number_day, not_even=True)
        else:   # Если завтрашний день в пределах до субботы, выводим завтрашнее расписание
            get_schedule(message, number_day)

    elif message.text == 'Другой день 🎓':
        print_even_week(message)    # Выводим какая сейчас неделя, чтобы было проще ориентироваться в выборе
        markup_week = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_even = types.KeyboardButton('Четная')
        button_not_even = types.KeyboardButton('Нечетная')
        button_menu = types.KeyboardButton('Меню')
        markup_week.add(button_even, button_not_even, button_menu)
        bot.send_message(message.chat.id, 'Какую неделю смотрим?', reply_markup=markup_week)

    elif message.text == 'Четная':
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

    elif message.text == 'Нечетная':
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
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    elif message.text == 'Вторник':
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    elif message.text == 'Среда':
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    elif message.text == 'Четверг':
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    elif message.text == 'Пятница':
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    elif message.text == 'Суббота':
        if message.chat.id - 1 == 'Четная':
            get_schedule(message, even=True)
        elif message.chat.id - 1 == 'Нечетная':
            get_schedule(message, not_even=True)
        else:
            get_schedule(message)

    else:
        bot.send_message(message.chat.id, 'Не знаю что делать =(')


bot.polling(none_stop=True, interval=0)
