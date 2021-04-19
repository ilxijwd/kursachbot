from telebot import TeleBot, types

bot = TeleBot("1698606681:AAH_XQtsvWBoF9pm5DIsW-4bJyjAJxDick0")

FULLNAME_IDS_TO_REPLY = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    identity_markup = types.InlineKeyboardMarkup()
    identity_markup.add(types.InlineKeyboardButton(text='👩‍🎓 Студент 👨‍🎓', callback_data='👩‍🎓 Студент 👨‍🎓'))
    identity_markup.add(types.InlineKeyboardButton(text='👩‍🏫 Керівник практики 👨‍🏫', callback_data='👩‍🏫 Керівник практики 👨‍🏫'))

    bot.send_message(msg.chat.id, "Привіт, ким будешь?", reply_markup=identity_markup)


@bot.callback_query_handler(func=lambda call: call.data == '👩‍🎓 Студент 👨‍🎓' or call.data == '👩‍🏫 Керівник практики 👨‍🏫')
def user_identity_query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Дякую за відповідь')
    bot.edit_message_text(f"Ви обрали: {call.data}", call.message.chat.id, call.message.message_id, reply_markup=None)

    fullname_reply_markup = types.ForceReply(selective=False)
    bot.send_message(call.message.chat.id, "Ваше ПІБ?", reply_markup=fullname_reply_markup)


@bot.message_handler(func=lambda msg: msg.chat.id > 0 and msg.chat.id in FULLNAME_IDS_TO_REPLY)
def get_user_fullname(msg):
    # TODO: FIND USER BY THIS FULLNAME IN DB, AND MAKE SURE HE'S FULLNAME NOT ALREADY TAKEN
    # TODO: LINK USER FULLNAME TO DB
    pass


bot.polling(none_stop=True)
