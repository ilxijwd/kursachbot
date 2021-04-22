from src.bot import tb
from src.db import session, Person, PlaceOfPractice


@tb.message_handler(
    func=lambda msg: hasattr(msg.reply_to_message, 'text') and msg.reply_to_message.text == "Вкажіть номер практики:"
)
def get_person_fullname(msg):
    person = session.query(Person).filter(Person.telegram_id == msg.chat.id).first()

    if not msg.text.isdigit():
        return tb.send_message(msg.chat.id, "Введіть порядковий номер місця практики зі списку доступних місць")

    place = session.query(PlaceOfPractice).filter(PlaceOfPractice.id == int(msg.text)).first()

    if not place:
        return tb.send_message(msg.chat.id, "Не знайдено жодного місця практики за цим номером")

    person.student.place_of_practice = place
    session.commit()

    tb.send_message(msg.chat.id, f"Ви успішно вибрали _{place.name}_ місцем практики", parse_mode='Markdown')
