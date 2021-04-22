from telebot import TeleBot

tb = TeleBot("1698606681:AAH_XQtsvWBoF9pm5DIsW-4bJyjAJxDick0")

from src.bot.listeners import *


def loop_over_requests():
    tb.polling(none_stop=True)
