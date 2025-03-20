import logging
from telethon import TelegramClient
from telethon.events import NewMessage
from general.schemas import EventTgSch
from general.scripts import (
    get_chat_with_thread_from_event,
    # get_one_event,
    define_event_and_add_to_database,
    take_event,
)


async def new_message_handler(new_message: NewMessage) -> None:
    # * Проверяем является сообщение альбомом
    if new_message.grouped_id:
        return
    client: TelegramClient = new_message.client
    event: EventTgSch | list[EventTgSch] = take_event(new_message)
    if not event:
        return
    event_with_chat_from_db = await define_event_and_add_to_database(event)
    if not event_with_chat_from_db:
        return
    
    if isinstance(event, list):
        event_with_chat_from_db = event_with_chat_from_db[0]
        event = event[0]
    chat_id, thread = await get_chat_with_thread_from_event(event_with_chat_from_db)

    await client.send_message(
        chat_id,
        message=new_message.message,
        reply_to=thread,
    )

    log_text = (
        f"Send simple message! Type:{event.type_of}Time:{event.time}Dvr:{event.dvr}"
    )

    logging.info(log_text)
