import logging
from telethon import TelegramClient
from telethon.events import NewMessage
from general.emun import EVENT_TYPE_THREAD
from general.scripts import take_event
from config import setting


async def new_message_handler(event: NewMessage) -> None:
    # async def handler(event: NewMessage.Event) -> None:
    client: TelegramClient = event.client
    ev = take_event(event)
    # print(client)
    if not ev:
        return

    event_type = ev.type_of.replace(" ", "_").upper()
    chat_thread = EVENT_TYPE_THREAD[event_type].value

    if event.grouped_id:
        return
    else:
        await client.send_message(
            int(setting.tg.send_chat_id),
            message=event.message,
            reply_to=chat_thread,
        )
        logging.info(
            f"Send simple message! Type:{ev.type_of} Time:{ev.time} Dvr:{ev.dvr}"
        )

    # return handler


#
