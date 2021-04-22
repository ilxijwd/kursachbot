import schedule
from datetime import datetime

from src.db import session, ExamMeeting
from src.bot import tb


def exam_meeting_notify():
    today = datetime.today()
    exam_meetings = session.query(ExamMeeting).all()
    for exam_meeting in exam_meetings:
        faculty = exam_meeting.head.faculty
        practice_term_start_date = faculty.practice_term.start_date.strptime("%Y-%m-%d")
        days_left_to_practice_start = (practice_term_start_date - today).days

        if 0 < days_left_to_practice_start <= 7:
            for group in faculty.groups:
                for student in group.students:
                    if student.person.telegram_id:
                        tb.send_message(
                            student.person.telegram_id,
                            f"Термін екзамену:\n\n"
                            f"*Дата*\n"
                            f"{exam_meeting.meeting.date}\n"
                            f"*Час початку*\n"
                            f"{exam_meeting.meeting.start_time}\n"
                            f"*Час завершення*\n"
                            f"{exam_meeting.meeting.end_time}\n"
                            f"*Місце проведення*\n"
                            f"{exam_meeting.meeting.place}",
                            parse_mode='Markdown',
                        )


schedule.every().day.at("08:00").do(exam_meeting_notify)
