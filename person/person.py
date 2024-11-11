import logging
from telethon import TelegramClient  # , events  # , sync
import sys


sys.path.append(".")
from config import setting
from activator import setup_handler

client = TelegramClient("session_name", setting.tg.api_id, setting.tg.api_hash)


async def main():
    await client.start()
    await setup_handler(client)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger("telethon").setLevel(level=logging.WARNING)
    logging.info("Person Bot Start!")
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())

# with open("data.json", "w", encoding="utf-8") as f:
#     f.write(json.dumps(result, ensure_ascii=False))
