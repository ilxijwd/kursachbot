import os

from telebot.types import ForceReply

from src.bot import tb
from src.db import session, Person, Student, PlaceOfPractice


@tb.message_handler(commands=['places'])
def places_command(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if not person:
        return tb.send_message(msg.chat.id, "Ви не зареєстровані")

    args = msg.text.split()[1:]
    if len(args) == 1:
        if args[0] == 'list':
            places = session.query(PlaceOfPractice).all()

            return tb.send_message(
                msg.chat.id,
                "Доступні місця практики:\n"
                f"{os.linesep.join((f'{i + 1}. {place.name}' for (i, place) in enumerate(places)))}",
                parse_mode='Markdown'
            )
        elif args[0] == 'take':
            if person.head:
                return tb.send_message(msg.chat.id, "Що, керівник, хочеш на практику?)")

            return tb.send_message(
                msg.chat.id,
                "Вкажіть номер практики:",
                reply_markup=ForceReply(selective=False)
            )
        elif args[0] == 'taken':
            if person.student:
                return tb.send_message(msg.chat.id, "В тебе немає доступу до цієї команди! 😡")

            determined_students = session.query(Student).filter(Student.place_of_practice).all()
            the_rest = session.query(Student).filter(not Student.place_of_practice).all()
            return tb.send_message(
                msg.chat.id,
                f"Вибрали місце практики: {len(determined_students)}\n"
                f"Не вибрали місце практики:\n"
                f"{os.linesep.join((f'{i + 1}. {student.person.fullname}' for (i, student) in enumerate(the_rest)))}",
                parse_mode='Markdown'
            )

    return tb.send_message(msg.chat.id, "Незнайомий аргумент, доступні: <list>, <take>, <taken>")
