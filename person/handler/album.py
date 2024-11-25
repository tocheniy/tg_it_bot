import logging
from telethon import TelegramClient
from telethon.events import Album
from general.emun import EVENT_TYPE_THREAD

# from config import setting
from general.schemas import EventTo
from general.scripts import (
    get_one_event,
    write_event_logs,
    take_event,
)


async def album_handler(album: Album) -> None:
    client: TelegramClient = album.client
    ev: EventTo | list[EventTo] = take_event(album)
    if not ev:
        return
    # print(ev)
    write_event_logs(ev)
    ev = get_one_event(ev)
    chat_id = ev.chat_id
    chat_thread = ev.thread
    files = [mes.media for mes in album.messages]
    # print(album.original_update.message.message)
    await client.send_file(
        chat_id,
        caption=album.original_update.message.message,
        file=files,
        reply_to=chat_thread,
    )

    log_text = (
        f"Send album message! Type:{ev.type_of}" f"Time:{ev.time}" f"Dvr:{ev.dvr}"
    )
    logging.info(log_text)
