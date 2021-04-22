import os
import schedule
from datetime import datetime

from src.db import session, Faculty
from src.bot import tb

from telebot.types import InputMediaDocument


def selected_place():
    documents = [
        open(os.path.join(os.path.dirname(os.getcwd()), 'паспорт_бази_практики.docx'), "rb"),
        open(os.path.join(os.path.dirname(os.getcwd()), 'договір.docx'), "rb")
    ]

    today = datetime.today()
    faculties = session.query(Faculty).all()
    for faculty in faculties:
        practice_term_start_date = faculty.practice_term.start_date.strptime("%Y-%m-%d")
        days_left_to_practice_start = (practice_term_start_date - today).days

        if 0 < days_left_to_practice_start <= 14:
            for group in faculty.groups:
                for student in group.students:
                    if student.person.telegram_id:
                        tb.send_message(
                            student.person.telegram_id,
                            "Ви ще не вибрали місце практики, "
                            "будь ласка ознайомтесь з переліком завдяки команді /places list "
                            "та виберіть один з доступних варіантів завдяки команді /places take.\n\n"
                            "Також оформить наступний перелік документів:",
                            parse_mode='Markdown',
                        )
                        tb.send_media_group(student.person.telegram_id, [InputMediaDocument(doc) for doc in documents])


schedule.every().day.at("08:00").do(selected_place)
