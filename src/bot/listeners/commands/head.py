from src.bot import tb
from src.db import session, Person


@tb.message_handler(commands=['head'])
def head_command(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if not person:
        return tb.send_message(msg.chat.id, "Ви не зареєстровані")

    if person.head:
        return tb.send_message(msg.chat.id, "Ви все про себе знаєте 😊")

    faculty = person.student.group.faculty
    tb.send_message(
        msg.chat.id,
        f"Керівником практики факультету *{faculty.short}* є"
        f"[{faculty.head.person.fullname}](https://t.me/user?id={faculty.head.person.telegram_id})",
        parse_mode='Markdown'
    )
