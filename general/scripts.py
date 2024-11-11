# scripts


from datetime import datetime
from general.schemas import EventTo


def take_event(msg) -> EventTo:
    msg_list = [item for item in msg.raw_text.split("\n") if item != ""]
    if len(msg_list) < 2:
        return

    event_type = ""
    event_time = ""
    dvr_name = ""
    camera_name = ""
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

    if all([event_type, event_time, dvr_name, camera_name]):
        ev = EventTo(
            type_of=event_type,
            time=event_time,
            dvr=dvr_name,
            camera=camera_name,
        )

    if all([event_type == "HDD Error", event_time, dvr_name]):
        ev = EventTo(
            type_of=event_type,
            time=event_time,
            dvr=dvr_name,
        )

    return ev
