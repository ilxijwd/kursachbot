from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


identity_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='👩‍🎓 Студент 👨‍🎓', callback_data='identity_markup=👩‍🎓 Студент 👨‍🎓')],
    [InlineKeyboardButton(text='👩‍🏫 Керівник 👨‍🏫', callback_data='identity_markup=👩‍🏫 Керівник 👨‍🏫')],
])
