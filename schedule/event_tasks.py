from datetime import datetime, timedelta

# from pprint import pprint
from telethon import TelegramClient
from database.crud.chat import get_chats
from database.crud.event import get_events_by_datetime_and_chat
from utils.data_work import make_statistic


async def send_statistics(ctx):
    client: TelegramClient = ctx["client"]

    day = datetime.now().date()
    prev_day = day - timedelta(hours=24, minutes=00, seconds=00)
    prev_day = str(prev_day)

    chats = await get_chats()
    if not chats:
        return

    # print(chats[0].tg_chat_id)
    for chat in chats:
        stat_thread = chat.statistic
        tg_chat_id = chat.tg_chat_id
        events = await get_events_by_datetime_and_chat(prev_day, tg_chat_id)
        if not events:
            return
        # print(events)

        res = []
        for index, ev in enumerate(events):
            ev_for_graphic = {
                "event_type": ev.event.name,
                "event_time": ev.event.time,
                "dvr_name": ev.name,
                "camera_name": ev.event.camera if ev.event.camera else None,
            }

            res.append(ev_for_graphic)

        files_src = make_statistic(res, tg_chat_id, prev_day, chat.name)
        cap = f"Статистика {chat.name} за {prev_day}"
        await client.send_file(
            tg_chat_id,
            caption=cap,
            file=files_src,
            reply_to=stat_thread,
        )
