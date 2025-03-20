from datetime import datetime
import json
import logging
import re
from telethon import TelegramClient  # , events  # , sync
import sys

from general.schemas import EventTgSch

sys.path.append(".")
from config import setting
# from activator import setup_handler

client = TelegramClient("session_name", setting.tg.api_id, setting.tg.api_hash)


def take_event(msg) -> EventTgSch | list[EventTgSch] | None:
    if not msg.raw_text:
        return None
    
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

    for item in msg_list:
        if "EVENT TYPE" in item:
            event_type = item.split(":")[1].strip()

        elif "EVENT TIME" in item:
            event_time = item.split(":", maxsplit=1)[1].strip()
            event_time = f"{datetime.strptime(event_time, '%Y-%m-%d,%H:%M:%S')}"

        elif "DVR NAME" in item:
            dvr_name = item.split(":")[1].strip()
            # city = dvr_name.split(" ")[2]

        elif "CAMERA NAME(NUM)" in item:
            camera_name = item.split(":")[1].strip()
            # (\w+|\w+\s\w+(\([A-Z]\d+\)\B))
            # "(\d+\s\w+\([A-Z]\d+\))"
            pattern = r"((\w+|\w+\s\w+)(\([A-Z]\d+\)))"
            cameras_names = [item[0] for item in re.findall(pattern, camera_name)]

    # ! Нужно удалить эту секцию

    # chats = setting.chats.result
    # city = city.lower()
    # if city not in ["msk", "vlg"]:
    #     city = "other"
    # city_chat = chats.get(city)
    # if city_chat is None:
    #     return None

    # chat_id = city_chat.get("chat_id")
    # ev_type_for_thread = event_type.lower().replace(" ", "_")
    # thread = city_chat.get("thread").get(ev_type_for_thread)

    # ! Конец

    tmp_dict = {
        "event_type": event_type,
        "event_time": event_time,
        "dvr_name": dvr_name,
    }
    if cameras_names and len(cameras_names) >= 2:
        for camera in cameras_names:
            tmp_dict.update({"camera_name": camera})

            result.append(tmp_dict)
        return result

    elif cameras_names:
        tmp_dict.update({"camera_name": cameras_names[0]})
        return tmp_dict

    elif event_type == "HDD Error":
        return tmp_dict


async def main():
    res = []
    await client.start()
    date = datetime(2025, 2, 5, 21)
    # print(date.)
    all_messages = await client.get_messages(
        entity=-1002456367513, reverse=True, offset_date=date
    )
    # for mes in all_messages[:5]:
    for mes in all_messages:
        event = take_event(mes)
        if not event:
            continue

        if isinstance(event, list):
            res.extend(event)
        else:
            res.append(event)
    
    # print(res)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False))
    
    # await setup_handler(client)
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # )
    # logging.getLogger("telethon").setLevel(level=logging.WARNING)
    # logging.info("Person Bot Start!")
    # await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())


