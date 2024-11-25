import logging
from telethon import TelegramClient
from telethon.events import NewMessage
from general.schemas import EventTo
from general.scripts import (
    get_one_event,
    write_event_logs,
    take_event,
)


async def new_message_handler(event: NewMessage) -> None:
    # * Проверяем является сообщение альбомом
    if event.grouped_id:
        return

    client: TelegramClient = event.client
    ev: EventTo | list[EventTo] = take_event(event)
    if not ev:
        return

    write_event_logs(ev)
    ev = get_one_event(ev)
    chat_id = ev.chat_id
    chat_thread = ev.thread

    await client.send_message(
        chat_id,
        message=event.message,
        reply_to=chat_thread,
    )

    log_text = (
        f"Send simple message! Type:{ev.type_of}" f"Time:{ev.time}" f"Dvr:{ev.dvr}"
    )

    logging.info(log_text)
