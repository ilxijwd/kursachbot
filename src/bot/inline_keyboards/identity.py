from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


identity_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='π©βπ Π‘ΡΡΠ΄Π΅Π½Ρ π¨βπ', callback_data='identity_markup=π©βπ Π‘ΡΡΠ΄Π΅Π½Ρ π¨βπ')],
    [InlineKeyboardButton(text='π©βπ« ΠΠ΅ΡΡΠ²Π½ΠΈΠΊ π¨βπ«', callback_data='identity_markup=π©βπ« ΠΠ΅ΡΡΠ²Π½ΠΈΠΊ π¨βπ«')],
])
