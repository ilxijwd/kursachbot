from os import path
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Text, Boolean, DateTime, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship, backref


db_path = path.join(path.dirname(__file__), 'kursachbot.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})
base = declarative_base()


class Faculty(base):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    short = Column(Text, unique=True)


class Specialty(base):
    __tablename__ = 'specialty'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    short = Column(Text, unique=True)


class Group(base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id"))
    faculty_id = Column(Integer, ForeignKey("faculty.id"))

    specialty = relationship("Specialty", backref="groups")
    faculty = relationship("Faculty", backref="groups")

    course = Column(Integer)
    subgroup = Column(Integer)


class PlaceOfPractice(base):
    __tablename__ = 'place_of_practice'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    info = Column(Text)


class Person(base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)

    telegram_id = Column(Integer, unique=True)
    fullname = Column(Text, unique=True)


class Student(base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    group_id = Column(Integer, ForeignKey("group.id"))
    place_of_practice_id = Column(Integer, ForeignKey("place_of_practice.id"))

    person = relationship("Person", backref=backref("student", uselist=False))
    group = relationship("Group", backref="students")
    place_of_practice = relationship("PlaceOfPractice", backref="students")

    has_debt = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Student(id={self.id}, ' \
               f'telegram_id={self.telegram_id}, ' \
               f'fullname={self.fullname}>'


class Meeting(base):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True)
    date = Column(Text)
    start_time = Column(Text)
    end_time = Column(Text)
    place = Column(Text)


class MeetingWithHead(base):
    __tablename__ = 'meeting_with_head'

    id = Column(Integer, primary_key=True)
    head_id = Column(Integer, ForeignKey("head.id"))
    meeting_id = Column(Integer, ForeignKey("meeting.id"))

    head = relationship("Head", backref=backref("meeting_with_head", uselist=False, cascade="all, delete"))
    meeting = relationship("Meeting", backref=backref("meeting_with_head", uselist=False, cascade="all, delete"))


class ScheduleMeeting(base):
    __tablename__ = 'schedule_meeting'

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    meeting_id = Column(Integer, ForeignKey("meeting.id"))

    schedule = relationship("Schedule", backref=backref("schedule_meetings", cascade="all, delete"))
    meeting = relationship("Meeting", backref=backref("schedule_meetings", cascade="all, delete"))


class ExamMeeting(base):
    __tablename__ = 'exam_meeting'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    meeting_id = Column(Integer, ForeignKey("meeting.id"))

    faculty = relationship("Faculty", backref=backref("exam_date", cascade="all, delete"))
    meeting = relationship("Meeting", backref=backref("exam_date", cascade="all, delete"))


class Head(base):
    __tablename__ = 'head'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    faculty_id = Column(Integer, ForeignKey("faculty.id"))

    person = relationship("Person", backref=backref("head", uselist=False))
    faculty = relationship("Faculty", backref=backref("head", uselist=False))


class Schedule(base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))

    faculty = relationship("Faculty", backref=backref("schedule", uselist=False))

    created_date = Column(DateTime, default=datetime.utcnow)


class PracticeTerm(base):
    __tablename__ = 'practice_term'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))

    faculty = relationship("Faculty", backref=backref("practice_term", uselist=False))

    start_date = Column(Text)
    end_date = Column(Text)


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
