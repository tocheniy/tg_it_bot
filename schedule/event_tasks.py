from datetime import datetime, timedelta

# from pprint import pprint
from telethon import TelegramClient
from database.crud.chat import get_chats
from database.crud.event import get_events_by_datetime_and_chat
from general.schemas import StatSch
from utils.data_work import make_statistic
from arq import Retry


async def send_statistics(ctx):
    try:
        client: TelegramClient = ctx["client"]
        logger = ctx["logger"]
        if not client.is_connected():
            logger.info("Переподключение к Telegram...")
            await client.connect()

        day = datetime.now().date()
        prev_day = day - timedelta(hours=24, minutes=00, seconds=00)
        prev_day = str(prev_day)

        chats = await get_chats()
        if not chats:
            raise Retry(defer=ctx["job_try"] * 5)
        # print(f"{len(chats)=}")
        for chat in chats:
            stat_thread = chat.statistic
            tg_chat_id = chat.tg_chat_id
            events = await get_events_by_datetime_and_chat(prev_day, tg_chat_id)
            if not events:
                logger.info(
                    f"У чата {tg_chat_id} | {chat.name} нет событий за {prev_day}"
                )
                continue

            res = []
            for ev in events:
                ev_for_graphic = {
                    "event_type": ev.event.name,
                    "event_time": ev.event.time,
                    "dvr_name": ev.name,
                    "camera_name": ev.event.camera if ev.event.camera else None,
                }

                res.append(ev_for_graphic)
            stats = make_statistic(res, tg_chat_id, prev_day, chat.name)
            if not stats:
                logger.info(
                    f"У чата {tg_chat_id} | {chat.name} нет статистики за {prev_day}"
                )
                continue
            # return
            cap = f"Статистика {chat.name} за {prev_day}\n\n"
            cap += f"{'-' * 20}\n"
            cap = get_cap_text(cap, stats)
            logger.info(f"Отправляем статистику в чат {tg_chat_id} | {chat.name}")
            # logger.info(f"Статистика: {cap}")
            await client.send_file(
                tg_chat_id,
                caption=cap,
                file=[stat.file_name for stat in stats],
                reply_to=stat_thread,
            )

    except Exception as Ex:
        logger.error(f"Ошибка при отправке статистики: {Ex}")
        raise Retry(defer=ctx["job_try"] * 5)


def get_cap_text(cap: str, stats: list[StatSch]):
    for stat in stats:
        # print(f"{stat.event_type} | кол-во: {stat.count}")
        event_type = get_ru_text_for_event_type(stat.event_type)
        cap += f"{event_type} | кол-во: {stat.count}\n"
        cap += f"{stat.data}\n"
        cap += f"{'-' * 20}\n"

    return cap


def get_ru_text_for_event_type(event_type):
    res = ""
    match event_type:
        case "View Tampering":
            res = "Перекрытия"
        case "HDD Error":
            res = "Жесткий диск"
        case "Video Signal Lost":
            res = "Потери видео"

    return res
