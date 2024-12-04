# scripts
import sys
import asyncio
from datetime import datetime
import logging
import re

from database.models.event import Event

if __name__ == "__main__":
    sys.path.append(".")
from database.crud.dvr import get_dvr_by_name
from database.crud.event import add_event
from general.schemas import EventModel, EventTo
from config import setting

logging.basicConfig(level=logging.DEBUG)
# * Обновляем чаты при запуске
setting.chats.update_data()


def take_event(msg) -> EventTo | list[EventTo] | None:
    msg_list = [item for item in msg.raw_text.split("\n") if item != ""]
    if len(msg_list) < 2:
        return None

    event_type = ""
    event_time = ""
    dvr_name = ""
    camera_name = ""
    city = ""
    chat_id = 0
    thread = 0
    cameras_names = []
    result = []
    ev: EventTo | None = None

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

    chats = setting.chats.result
    city = city.lower()
    if city not in ["msk", "vlg"]:
        city = "other"
    city_chat = chats.get(city)
    if city_chat is None:
        return None
    chat_id = city_chat.get("chat_id")

    ev_type_for_thread = event_type.lower().replace(" ", "_")
    thread = city_chat.get("thread").get(ev_type_for_thread)

    ev = EventTo(
        type_of=event_type,
        time=event_time,
        dvr=dvr_name,
        city=city,
        chat_id=chat_id,
        thread=thread,
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


def get_one_event(ev: EventTo | list[EventTo]) -> EventTo:
    if isinstance(ev, list):
        return ev[0]
    return ev


async def define_event_and_add_to_database(
    events: EventTo | list[EventTo],
) -> list[Event] | Event | None:
    if isinstance(events, list) and len(events) >= 2:
        res = []
        for evnt in events:
            event_from_db = await add_event_to_db(evnt)
            if not event_from_db:
                continue
            res.append(event_from_db)
            display_event_log(evnt)
        if not res:
            return None
        return res

    elif isinstance(events, EventTo):
        event_from_db = await add_event_to_db(events)
        if not event_from_db:
            return None
        display_event_log(events)
        return event_from_db


async def add_event_to_db(event: EventTo) -> Event | None:
    dvr = await get_dvr_by_name(event.dvr)
    if not dvr:
        return
    event = EventModel(
        dvr_id=dvr.id,
        name=event.type_of,
        camera=event.camera,
        time=event.time,
    )
    # print(event)
    event = await add_event(event)
    if not event:
        return None
    return event


def display_event_log(event: EventTo):
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


# async def main():
#     ev = [
#         EventTo(
#             type_of="dsadas",
#             time=datetime.now(),
#             camera="Cam",
#             dvr="Reg 1 VLG",
#             city="MSK",
#         ),
#         EventTo(
#             type_of="dsadas",
#             time=datetime.now(),
#             camera="Cam",
#             dvr="Reg 1 VLG",
#             city="MSK",
#         ),
#     ]
#     await define_event_and_add_to_database(ev)


# if __name__ == "__main__":
#     asyncio.run(main())
