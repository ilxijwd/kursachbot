from telebot.types import ForceReply

from src.bot import tb


@tb.callback_query_handler(func=lambda call: call.data.startswith('identity_markup='))
def user_identity_query_handler(call):
    tb.edit_message_text(
        f"Ви обрали: *{call.data.split('identity_markup=')[1]}*",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
        parse_mode='Markdown'
    )

    tb.answer_callback_query(callback_query_id=call.id)
    tb.send_message(call.message.chat.id, "Ваше ПІБ?", reply_markup=ForceReply(selective=False))
