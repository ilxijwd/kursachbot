from os import path
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship, backref


db_path = path.join(path.dirname(__file__), 'kursachbot.db')
engine = create_engine(f'sqlite:///{db_path}')
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

    course = Column(Integer)
    subgroup = Column(Integer)

    specialty = relationship("Specialty", backref="groups")
    faculty = relationship("Faculty", backref="groups")


class PlaceOfPractice(base):
    __tablename__ = 'place_of_practice'

    id = Column(Integer, primary_key=True)
    info = Column(Text)


class Student(base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"))
    place_of_practice_id = Column(Integer, ForeignKey("place_of_practice.id"))

    telegram_id = Column(Integer, unique=True)
    fullname = Column(Text, unique=True)

    group = relationship("Group", backref="students")
    place_of_practice = relationship("PlaceOfPractice", backref="students")

    def __repr__(self):
        return f'<Student(id={self.id}, ' \
               f'telegram_id={self.telegram_id}, ' \
               f'fullname={self.fullname}>'


class Head(base):
    __tablename__ = 'head'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"))

    telegram_id = Column(Integer, unique=True)
    fullname = Column(Text, unique=True)

    group = relationship("Group", backref=backref("head", uselist=False))


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


FACULTIES = [
    Faculty(name="Інфокомунікацій та програмної інженерії", short="ІКПІ"),
]

SPECIALITIES = [
    Specialty(name="Комп'ютерні науки", short="КН")
]

GROUPS = [
    Group(course=3, subgroup=1, specialty=SPECIALITIES[0], faculty=FACULTIES[0])
]

PLACE_OF_PRACTICES = [
    PlaceOfPractice(info="Державний університет інтелектуальних технологій і зв'язку"),
    PlaceOfPractice(info="KeepSolid Inc."),
    PlaceOfPractice(info="Google Inc."),
]

STUDENTS = [
    Student(fullname="Петров В. О.", group=GROUPS[0]),
    Student(fullname="Казимир В. О.", group=GROUPS[0]),
    Student(fullname="Журний Р. С.", group=GROUPS[0]),
]

HEADS = [
    Head(fullname="Пупкін Б. Р.", group=GROUPS[0])
]

for faculty in FACULTIES:
    search = session.query(Faculty).filter(Faculty.name == faculty.name).first()

    if not search:
        session.add(faculty)

session.commit()

for specialty in SPECIALITIES:
    search = session.query(Specialty).filter(Specialty.name == specialty.name).first()

    if not specialty:
        session.add(specialty)

session.commit()

for group in GROUPS:
    search = session.query(Group).filter((Group.specialty == group.specialty) & (Group.faculty == group.specialty)).first()

    if not search:
        session.add(group)

session.commit()

for placeOfPractice in PLACE_OF_PRACTICES:
    search = session.query(PlaceOfPractice).filter(PlaceOfPractice.info == placeOfPractice.info).first()

    if not search:
        session.add(placeOfPractice)

session.commit()

for student in STUDENTS:
    search = session.query(Student).filter(Student.fullname == student.fullname).first()

    if not search:
        session.add(student)

session.commit()

for head in HEADS:
    search = session.query(Head).filter(Head.fullname == head.fullname).first()

    if not search:
        session.add(head)

session.commit()
