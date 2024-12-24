import logging
from telethon import TelegramClient
from telethon.events import Album

from general.schemas import EventTgSch
from general.scripts import (
    get_one_event,
    define_event_and_add_to_database,
    take_event,
)
# from database.crud.dvr import get_dvr_by_name


async def album_handler(album: Album) -> None:
    client: TelegramClient = album.client
    ev: EventTgSch | list[EventTgSch] = take_event(album)
    if not ev:
        return

    event_from_db = await define_event_and_add_to_database(ev)
    if not event_from_db:
        return

    ev = get_one_event(ev)
    chat_id = ev.chat_id
    chat_thread = ev.thread
    files = [mes.media for mes in album.messages]
    await client.send_file(
        chat_id,
        caption=album.original_update.message.message,
        file=files,
        reply_to=chat_thread,
    )

    log_text = (
        f"Send album message! Type:{ev.type_of}" f" | Time:{ev.time}" f" | Dvr:{ev.dvr}"
    )
    logging.info(log_text)
