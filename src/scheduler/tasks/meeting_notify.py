import schedule
from datetime import datetime

from src.db import session, MeetingWithHead
from src.bot import tb


def meeting_notify():
    today = datetime.today()
    meetings_with_head = session.query(MeetingWithHead).all()
    for meeting_with_head in meetings_with_head:
        faculty = meeting_with_head.head.faculty
        practice_term_start_date = faculty.practice_term.start_date.strptime("%Y-%m-%d")
        days_left_to_practice_start = (practice_term_start_date - today).days

        if 0 < days_left_to_practice_start <= 7:
            for group in faculty.groups:
                for student in group.students:
                    if student.person.telegram_id:
                        tb.send_message(
                            student.person.telegram_id,
                            f"Зустріч з керівником практики запланована на:\n\n"
                            f"*Дата*\n"
                            f"{meeting_with_head.meeting.date}\n"
                            f"*Час початку*\n"
                            f"{meeting_with_head.meeting.start_time}\n"
                            f"*Час завершення*\n"
                            f"{meeting_with_head.meeting.end_time}\n"
                            f"*Місце проведення*\n"
                            f"{meeting_with_head.meeting.place}",
                            parse_mode='Markdown',
                        )


schedule.every().day.at("08:00").do(meeting_notify)
