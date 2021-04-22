from src.bot import tb
from src.bot.inline_keyboards import identity_markup
from src.db import session, Person


@tb.message_handler(commands=['start'])
def send_welcome(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if person:
        return tb.send_message(msg.chat.id, f"Привіт {person.fullname} 😊")

    tb.send_message(msg.chat.id, "Привіт, ким ти є?", reply_markup=identity_markup)
