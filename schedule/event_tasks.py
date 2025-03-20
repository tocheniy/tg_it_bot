from datetime import datetime, timedelta
from pprint import pprint
from telethon import TelegramClient
# from telethon.tl.types import PeerChat, PeerUser

from database.crud.chat import get_chats
from database.crud.event import get_events_by_datetime, get_events_by_datetime_and_chat
from utils.data_work import make_statistic_graphic


async def send_statistics(ctx):
    client: TelegramClient = ctx["client"]
    text = """Текст текст"""
    day = datetime.now().date()
    prev_day = datetime.now().date() - timedelta(hours=24, minutes=00, seconds=00)
    prev_day = str(prev_day)
    # date_str = datetime.strptime(

    chats = await get_chats()
    if not chats:
        return

    # print(chats[0].tg_chat_id)
    for chat in chats:
        events = await get_events_by_datetime_and_chat(prev_day, chat.tg_chat_id)
        if not events:
            return
        print(chat.tg_chat_id)
        print(len(events))

    # events = await get_events_by_datetime(prev_day)
    if not events:
        return
    # print(events)
    res = []
    for ev in events:
        ev_for_graphic = {
            "event_type": ev.event.name,
            "event_time": ev.event.time,
            "dvr_name": ev.name,
            "camera_name": ev.event.camera if ev.event.camera else None,
        }
        res.append(ev_for_graphic)

    # pprint(res)
    # make_statistic_graphic(res)

    # user = await client.get_entity('@suhanov_alex')
    # user = PeerUser(user_id=6920661749)
    # if not user:
    #     return
    # print(user)
    # await client.send_message(6920661749, message=text)
