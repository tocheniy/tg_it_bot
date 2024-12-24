import logging
from telethon import TelegramClient
from telethon.events import NewMessage
from general.schemas import EventTgSch
from general.scripts import (
    get_one_event,
    define_event_and_add_to_database,
    take_event,
)


async def new_message_handler(event: NewMessage) -> None:
    # * Проверяем является сообщение альбомом
    if event.grouped_id:
        return

    client: TelegramClient = event.client
    ev: EventTgSch | list[EventTgSch] = take_event(event)
    if not ev:
        return

    event_from_db = await define_event_and_add_to_database(ev)
    if not event_from_db:
        return
    
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
