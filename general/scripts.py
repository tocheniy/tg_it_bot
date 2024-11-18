# scripts
from datetime import datetime
import logging
import re
from general.schemas import EventTo


def take_event(msg) -> EventTo | list[EventTo] | None:
    msg_list = [item for item in msg.raw_text.split("\n") if item != ""]
    if len(msg_list) < 2:
        return None

    event_type = ""
    event_time = ""
    dvr_name = ""
    camera_name = ""
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

        elif "CAMERA NAME(NUM)" in item:
            camera_name = item.split(":")[1].strip()
            # (\w+|\w+\s\w+(\([A-Z]\d+\)\B))
            # "(\d+\s\w+\([A-Z]\d+\))"
            pattern = r"((\w+|\w+\s\w+)(\([A-Z]\d+\)))"
            cameras_names = [item[0] for item in re.findall(pattern, camera_name)]

    if cameras_names and len(cameras_names) >= 2:
        for camera in cameras_names:
            result.append(
                EventTo(
                    type_of=event_type,
                    time=event_time,
                    dvr=dvr_name,
                    camera=camera,
                )
            )
        return result
    elif cameras_names:
        ev = EventTo(
            type_of=event_type,
            time=event_time,
            dvr=dvr_name,
            camera=cameras_names[0],
        )
        return ev

    elif event_type == "HDD Error":
        ev = EventTo(
            type_of=event_type,
            time=event_time,
            dvr=dvr_name,
            # camera=camera,
        )
        return ev


def is_list(ev):
    if not isinstance(ev, list):
        return False
    return True


def retn_event_type_with_logs(events: EventTo | list[EventTo]):
    if isinstance(events, list) and len(events) >= 2:
        for evnt in events:
            log_text = (
                f"LOGS_MAIN#EVENTS Type:{evnt.type_of}"
                f" | Time:{evnt.time}"
                f" | Dvr:{evnt.dvr}"
                f" | Cam: {evnt.camera}"
            )
            logging.info(log_text)
        return evnt.type_of

    elif isinstance(events, EventTo):
        # print(events)
        log_text = (
            f"LOGS_MAIN#EVENTS Type:{events.type_of}"
            f" | Time:{events.time}"
            f" | Dvr:{events.dvr}"
        )
        if events.camera:
            log_text += f" | Cam: {events.camera}"
        logging.info(log_text)
        return events.type_of
