from .models import session, Faculty, Specialty, Group, PlaceOfPractice, Person, Student, Head, Schedule, Meeting, MeetingWithHead, ScheduleMeeting, PracticeTerm, ExamMeeting


def initiate():
    faculties = [
        Faculty(name="Інфокомунікацій та програмної інженерії", short="ІКПІ"),
    ]

    practice_terms = [
        PracticeTerm(faculty=faculties[0], start_date="2021-06-24", end_date="2021-07-18")
    ]

    specialities = [
        Specialty(name="Комп'ютерні науки", short="КН"),
    ]

    groups = [
        Group(course=3, subgroup=1, specialty=specialities[0], faculty=faculties[0]),
    ]

    place_of_practices = [
        PlaceOfPractice(name="Державний університет інтелектуальних технологій і зв'язку"),
        PlaceOfPractice(name="KeepSolid Inc."),
        PlaceOfPractice(name="Google Inc."),
    ]

    persons = [
        Person(fullname="Петров В. О."),
        Person(fullname="Казимир В. О."),
        Person(fullname="Журний Р. С."),
        Person(fullname="Пупкін Б. Р."),
    ]

    students = [
        Student(person=persons[0], group=groups[0]),
        Student(person=persons[1], group=groups[0], has_debt=True),
        Student(person=persons[2], group=groups[0]),
    ]

    heads = [
        Head(person=persons[3], faculty=faculties[0]),
    ]

    meetings_with_head = [
        MeetingWithHead(
            head=heads[0],
            meeting=Meeting(
                date="2021-07-16",
                start_time="9:00",
                end_time="12:00",
                place="Аудиторія 310, головний корпус"
            )
        )
    ]

    exam_meetings = [
        ExamMeeting(
            faculty=faculties[0],
            meeting=Meeting(
                date="2021-07-17",
                start_time="9:00",
                end_time="12:00",
                place="Аудиторія 310, головний корпус"
            )
        )
    ]

    for faculty in faculties:
        search = session.query(Faculty).filter(Faculty.name == faculty.name).first()

        if not search:
            session.add(faculty)

    for practice_term in practice_terms:
        faculty = session.query(Faculty).filter(Faculty.name == practice_term.faculty.name).first()
        search = session.query(PracticeTerm).filter(PracticeTerm.faculty == faculty).first()

        if not search:
            session.add(practice_term)

    for specialty in specialities:
        search = session.query(Specialty).filter(Specialty.name == specialty.name).first()

        if not search:
            session.add(specialty)

    for group in groups:
        faculty = session.query(Faculty).filter(Faculty.name == group.faculty.name).first()
        specialty = session.query(Specialty).filter(Specialty.name == group.specialty.name).first()
        search = session.query(Group).filter((Group.specialty == specialty) & (Group.faculty == faculty)).first()

        if not search:
            session.add(group)

    for place_of_practice in place_of_practices:
        search = session.query(PlaceOfPractice).filter(PlaceOfPractice.name == place_of_practice.name).first()

        if not search:
            session.add(place_of_practice)

    for person in persons:
        search = session.query(Person).filter(Person.fullname == person.fullname).first()

        if not search:
            session.add(person)

    for student in students:
        person = session.query(Person).filter(Person.fullname == student.person.fullname).first()
        search = session.query(Student).filter(Student.person == person).first()

        if not search:
            session.add(student)

    for head in heads:
        person = session.query(Person).filter(Person.fullname == head.person.fullname).first()
        search = session.query(Head).filter(Head.person == person).first()

        if not search:
            session.add(head)

    for meeting_with_head in meetings_with_head:
        search = session.query(MeetingWithHead).filter(
            (MeetingWithHead.meeting == meeting_with_head.meeting) &
            (MeetingWithHead.head == meeting_with_head.head)
        )

        if not search:
            session.add(meeting_with_head)

    for exam_meeting in exam_meetings:
        search = session.query(ExamMeeting).filter(
            (ExamMeeting.meeting == exam_meeting.meeting) &
            (ExamMeeting.faculty == exam_meeting.faculty)
        )

        if not search:
            session.add(exam_meeting)

    session.commit()


initiate()
