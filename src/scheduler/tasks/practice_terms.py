import schedule
from datetime import datetime

from src.db import session, Faculty
from src.bot import tb


def practice_terms():
    today = datetime.today()
    faculties = session.query(Faculty).all()
    for faculty in faculties:
        practice_term_start_date = faculty.practice_term.start_date.strptime("%Y-%m-%d")
        practice_term_end_date = faculty.practice_term.start_date.strptime("%Y-%m-%d")
        days_left_to_practice_start = (practice_term_start_date - today).days

        if 0 < days_left_to_practice_start <= 3:
            for group in faculty.groups:
                for student in group.students:
                    if student.person.telegram_id:
                        tb.send_message(
                            student.person.telegram_id,
                            f"Кількість днів до початку практики: {days_left_to_practice_start}\n\n"
                            f"*Дата початку практики*\n"
                            f"{practice_term_end_date}\n\n"
                            f"*Дата завершення практики*\n"
                            f"{practice_term_end_date}",
                            parse_mode='Markdown'
                        )


schedule.every().day.at("08:00").do(practice_terms)
