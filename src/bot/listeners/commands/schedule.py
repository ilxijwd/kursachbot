import os

from telebot.types import ForceReply

from src.bot import tb
from src.db import session, Person, Student, PlaceOfPractice


@tb.message_handler(commands=['schedule'])
def schedule_command(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()
    if not person:
        return tb.send_message(msg.chat.id, "Ви не зареєстровані")

    args = msg.text.split()[1:]
    if len(args) == 1:
        if args[0] == 'change':
            if person.student:
                return tb.send_message(msg.chat.id, "В тебе немає доступу до цієї команди! 😡")

            return tb.send_message(msg.chat.id, "Очікую файл розкладу", reply_markup=ForceReply(selective=False))
        elif args[0] == 'show':
            schedule = None

            if person.student:
                schedule = person.student.group.faculty.schedule
            elif person.head:
                schedule = person.head.faculty.schedule

            if not schedule:
                return tb.send_message(msg.chat.id, "Розкладу поки що немає 😢")

            return tb.send_message(
                msg.chat.id,
                f"Розклад консультацій від *{schedule.created_date.strftime('%Y-%m-%d')}*:\n\n"
                "\n".join((
                    f"*Дата*\n"
                    f"{schedule_meeting.meeting.date}\n"
                    f"*Час початку*\n"
                    f"{schedule_meeting.meeting.start_time}\n"
                    f"*Час завершення*\n"
                    f"{schedule_meeting.meeting.end_time}\n"
                    f"*Місце проведення*\n"
                    f"{schedule_meeting.meeting.place}\n" for schedule_meeting in schedule.schedule_meetings
                )),
                parse_mode='Markdown'
            )

    return tb.send_message(msg.chat.id, "Незнайомий аргумент, доступні: <change>, <show>")
