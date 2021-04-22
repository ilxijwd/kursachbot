from sqlalchemy import func

from src.bot import tb
from src.db import session, Person, Student


@tb.message_handler(func=lambda msg: hasattr(msg.reply_to_message, 'text') and msg.reply_to_message.text == "Ваше ПІБ?")
def get_schedule_file(msg):
    person = session.query(Person).filter(func.lower(Person.fullname) == func.lower(msg.text)).first()

    if not person:
        return tb.send_message(
            msg.chat.id,
            f"Такого ПІБ немає у базі, зв'яжіться з [адміністратором](https://t.me/Regis322)",
            parse_mode='Markdown'
        )

    if person.telegram_id:
        return tb.send_message(
            msg.chat.id,
            "Людина за цим ПІБ вже зареэстрована, зв'яжіться з [адміністратором](https://t.me/Regis322)",
            parse_mode='Markdown'
        )

    person.telegram_id = msg.chat.id
    session.add(person)
    session.commit()

    tb.send_message(msg.chat.id, "Ваш ПІБ знайдено у базі, ваш телеграм під'єднано")