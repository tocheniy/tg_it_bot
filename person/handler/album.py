import logging
from telethon import TelegramClient
from telethon.events import Album

from general.schemas import EventTgSch
from general.scripts import (
    get_chat_with_thread_from_event,
    # get_one_event,
    define_event_and_add_to_database,
    take_event,
)
# from database.crud.dvr import get_dvr_by_name


async def album_handler(album: Album) -> None:
    client: TelegramClient = album.client
    # * События
    event = take_event(album)
    if not event:
        return

    event_with_chat_from_db = await define_event_and_add_to_database(event)
    if not event_with_chat_from_db:
        return
    
    if isinstance(event, list):
        event_with_chat_from_db = event_with_chat_from_db[0]
        event = event[0]
    
    chat_id, thread = await get_chat_with_thread_from_event(event_with_chat_from_db)
    files = [mes.media for mes in album.messages]
    await client.send_file(
        chat_id,
        caption=album.original_update.message.message,
        file=files,
        reply_to=thread,
    )

    log_text = (
        f"Send album message! Type:{event.type_of}"
        f" | Time:{event.time}"
        f" | Dvr:{event.dvr}"
    )
    logging.info(log_text)
