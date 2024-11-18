import logging
from telethon import TelegramClient
from telethon.events import Album
from general.emun import EVENT_TYPE_THREAD

from config import setting
from general.schemas import EventTo
from general.scripts import (
    # convert_to_list_or_ev,
    is_list,
    retn_event_type_with_logs,
    take_event,
)


async def album_handler(album: Album) -> None:
    client: TelegramClient = album.client
    ev: EventTo | list[EventTo] = take_event(album)
    if not ev:
        return
    # print(ev)
    ev_type = retn_event_type_with_logs(ev)
    ev_type = ev_type.replace(" ", "_").upper()
    chat_thread = EVENT_TYPE_THREAD[ev_type].value
    files = [mes.media for mes in album.messages]
    # print(album.original_update.message.message)
    await client.send_file(
        int(setting.tg.send_chat_id),
        caption=album.original_update.message.message,
        file=files,
        reply_to=chat_thread,
    )

    log_text = (
        f"Send album message! Type:{ev[0].type_of if is_list(ev) else ev.type_of}"
        f"Time:{ev[0].time if is_list(ev) else ev.time}"
        f"Dvr:{ev[0].dvr if is_list(ev) else ev.dvr}"
    )
    logging.info(log_text)
