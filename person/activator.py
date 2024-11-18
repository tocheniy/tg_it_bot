# import logging
# from general.emun import EVENT_TYPE_THREAD
# from person.person import client

from handler.newmessage import new_message_handler

from handler.album import album_handler
from telethon import TelegramClient
from telethon.events import NewMessage, Album
from config import setting
# from utils.scripts import take_event

chats = setting.tg.chans_ids_convert()


async def setup_handler(client: TelegramClient):
    client.add_event_handler(
        album_handler,
        Album(chats=chats),
    )
    client.add_event_handler(
        new_message_handler,
        NewMessage(chats=chats),
    )
