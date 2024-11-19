import logging
from telethon import TelegramClient
from telethon.events import NewMessage
from general.emun import EVENT_TYPE_THREAD
from general.schemas import EventTo
from general.scripts import (
    is_list,
    retn_event_type_with_logs,
    take_event,
)
from config import setting


async def new_message_handler(event: NewMessage) -> None:
    # * Проверяем является сообщение альбомом
    if event.grouped_id:
        return

    client: TelegramClient = event.client
    ev: EventTo | list[EventTo] = take_event(event)
    if not ev:
        return

    ev_type = retn_event_type_with_logs(ev)
    ev_type = ev_type.replace(" ", "_").upper()
    chat_thread = EVENT_TYPE_THREAD[ev_type].value

    await client.send_message(
        int(setting.tg.send_chat_id),
        message=event.message,
        reply_to=chat_thread,
    )

    log_text = (
        f"Send simple message! Type:{ev[0].type_of if is_list(ev) else ev.type_of}"
        f"Time:{ev[0].time if is_list(ev) else ev.time}"
        f"Dvr:{ev[0].dvr if is_list(ev) else ev.dvr}"
    )
    logging.info(log_text)
