# scripts
import asyncio
import sys

# import asyncio
from datetime import datetime
import logging
import re

if __name__ == "__main__":
    sys.path.append(".")
from database.crud.dvr import get_dvr_by_name
from database.crud.event import add_event
from general.schemas import EventDbSch, EventTgSch, EventWithChat
from config import setting

logging.basicConfig(level=logging.DEBUG)
# * Обновляем чаты при запуске
setting.chats.update_data()


def take_event(msg) -> EventTgSch | list[EventTgSch] | None:
    msg_list = [item for item in msg.raw_text.split("\n") if item != ""]
    if len(msg_list) < 2:
        return None

    event_type = ""
    event_time = ""
    dvr_name = ""
    camera_name = ""
    city = ""
    cameras_names = []
    result = []
    ev: EventTgSch | None = None

    for item in msg_list:
        if "EVENT TYPE" in item:
            event_type = item.split(":")[1].strip()

        elif "EVENT TIME" in item:
            event_time = item.split(":", maxsplit=1)[1].strip()
            event_time = f"{datetime.strptime(event_time, '%Y-%m-%d,%H:%M:%S')}"

        elif "DVR NAME" in item:
            dvr_name = item.split(":")[1].strip()
            city = dvr_name.split(" ")[2]

        elif "CAMERA NAME(NUM)" in item:
            camera_name = item.split(":")[1].strip()
            # (\w+|\w+\s\w+(\([A-Z]\d+\)\B))
            # "(\d+\s\w+\([A-Z]\d+\))"
            pattern = r"((\w+|\w+\s\w+)(\([A-Z]\d+\)))"
            cameras_names = [item[0] for item in re.findall(pattern, camera_name)]

    ev = EventTgSch(
        type_of=event_type,
        time=event_time,
        dvr=dvr_name,
        city=city,
    )

    if cameras_names and len(cameras_names) >= 2:
        for camera in cameras_names:
            ev = ev.model_copy(deep=True)
            ev.camera = camera
            result.append(ev)
        return result

    elif cameras_names:
        ev.camera = cameras_names[0]
        return ev

    elif event_type == "HDD Error":
        return ev


async def define_event_and_add_to_database(
    events: EventTgSch | list[EventTgSch],
) -> list[EventWithChat] | EventWithChat | None:
    if isinstance(events, list) and len(events) >= 2:
        res = []
        for evnt in events:
            event_with_chat = await add_event_to_db_and_return_event_with_chat(evnt)
            if not event_with_chat:
                continue
            res.append(event_with_chat)
            display_event_log(evnt)
        if not res:
            return None
        return res

    elif isinstance(events, EventTgSch):
        event_with_chat = await add_event_to_db_and_return_event_with_chat(events)
        if not event_with_chat:
            return None
        display_event_log(events)
        return event_with_chat


async def add_event_to_db_and_return_event_with_chat(
    event: EventTgSch,
) -> EventWithChat | None:
    dvr = await get_dvr_by_name(event.dvr)
    if not dvr:
        return
    division = dvr.division
    chat = division.chat
    event_to_db = EventDbSch(
        dvr_id=dvr.id,
        name=event.type_of,
        camera=event.camera,
        time=event.time,
    )
    event_with_chat = EventWithChat(chat=chat, event=event_to_db)
    # * for test
    test = "TEST"
    width = 18
    symbol = "_-*-_"
    symbol_quant = 5
    test_header = (
        f"{symbol * symbol_quant:<20}{test:^{width}}{symbol * symbol_quant:>20}"
    )
    if event.type_of == test:
        print(test_header)
        print(event_with_chat.event)
        print(event_with_chat.chat)
        symbol = "¯-*-¯"
        test_header = (
            f"{symbol * symbol_quant:<20}{test:^{width}}{symbol * symbol_quant:>20}"
        )
        print(test_header)
        print()
        return event_with_chat

    event_from_db = await add_event(event_to_db)
    if not event_from_db:
        return None
    return event_with_chat


def display_event_log(event: EventTgSch):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    log_text = (
        f"LOGS_MAIN#EVENTS Type: {event.type_of}"
        f" | Time: {event.time.strftime(datetime_format)}"
        f" | City: {event.city}"
        f" | Dvr: {event.dvr}"
    )
    if event.camera:
        log_text += f" | Cam: {event.camera}"
    logging.info(log_text)


async def get_chat_with_thread_from_event(event_with_chat: EventWithChat):
    event = event_with_chat.event
    chat = event_with_chat.chat

    type_name = event.name.lower().replace(" ", "_")
    chat_id = chat.tg_chat_id
    thread = chat.__getattribute__(type_name)
    return chat_id, thread


async def main():
    ev = [
        EventTgSch(
            type_of="TEST",
            time=datetime.now(),
            camera="Cam",
            dvr="Reg 1 VLG",
            city="MSK",
        ),
        EventTgSch(
            type_of="TEST",
            time=datetime.now(),
            camera="Cam",
            dvr="Reg 1 MSK",
            city="MSK",
        ),
        EventTgSch(
            type_of="TEST",
            time=datetime.now(),
            camera="Cam",
            dvr="Reg 1 STAR POLT",
            city="STAR POLT",
        ),
    ]
    await define_event_and_add_to_database(ev)


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(main())
    # asyncio.run(main())
