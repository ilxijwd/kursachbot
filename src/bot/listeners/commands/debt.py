import os

from src.bot import tb
from src.db import session, Person, Student


@tb.message_handler(commands=['dept'])
def dept_command(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if not person:
        return tb.send_message(msg.chat.id, "Ви не зареєстровані")

    args = msg.text.split()[1:]
    if len(args) == 1:
        if args[0] == 'list':
            if not person.head:
                return tb.reply_to(msg, "У вас нема доступа до цієї команди")

            students_with_dept = session.query(Student).filter(Student.has_debt).all()

            if len(students_with_dept) > 0:
                return tb.send_message(
                    msg.chat.id,
                    "Студенти які мають борг:\n"
                    f"{os.linesep.join((f'{i + 1}. {student.person.fullname}' for (i, student) in enumerate(students_with_dept)))}",
                    parse_mode='Markdown'
                )
            else:
                return tb.send_message(msg.chat.id, "Немає студентів з боргом")
        else:
            return tb.send_message(msg.chat.id, "Незнайомий аргумент, доступні: <list>")

    if person.head:
        return tb.send_message(msg.chat.id, "У керівника не може бути боргу 😂")

    tb.send_message(
        msg.chat.id,
        "У вас є борг по практиці" if person.student.has_debt else 'У вас немає боргу по практиці'
    )
