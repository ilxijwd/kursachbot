import os

from src.bot import tb
from src.db import session, Person


@tb.message_handler(commands=['inform'])
def inform_command(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if not person:
        return tb.send_message(msg.chat.id, "Ви не зареєстровані")

    if person.student:
        return tb.send_message(msg.chat.id, "Ця команда для керівників практики!")

    not_informed_students = []
    informed_students = []
    args = msg.text.split()[1:]
    if len(args) > 1:
        inform_message = ' '.join(args)
        for group in person.faculty.groups:
            for student in group.students:
                if not student.person.telegram_id:
                    not_informed_students.append(student)
                    continue

                tb.send_message(student.person.telegram_id, inform_message)
                informed_students.append(student)

    tb.send_message(
        msg.chat.id,
        f"Інформованих студентів: {len(informed_students)}\n"
        "Не отримали повідомленя: \n"
        f"{os.linesep.join((f'{i + 1}. {student.person.fullname}' for (i, student) in enumerate(not_informed_students)))}",
        parse_mode='Markdown'
    )
