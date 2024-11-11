import logging
from telethon import TelegramClient
from telethon.events import Album
from general.emun import EVENT_TYPE_THREAD

from config import setting
from general.scripts import take_event


async def album_handler(album: Album) -> None:
    client: TelegramClient = album.client
    ev = take_event(album)

    event_type = ev.type_of.replace(" ", "_").upper()
    chat_thread = EVENT_TYPE_THREAD[event_type].value

    files = [mes.media for mes in album.messages]
    await client.send_file(
        int(setting.tg.send_chat_id),
        caption=album.original_update.message.message,
        file=files,
        reply_to=chat_thread,
    )
    logging.info(
        f"Send mediagroup message! Type:{ev.type_of} | Time:{ev.time} | Dvr:{ev.dvr}"
    )

    
