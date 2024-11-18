from telethon import TelegramClient
from telethon.tl.types import PeerChat, PeerUser


async def send_message(ctx):
    client: TelegramClient = ctx["client"]
    text = ctx["text"]
    # user = await client.get_entity('@suhanov_alex')
    # user = PeerUser(user_id=6920661749)
    # if not user:
    #     return
    # print(user)
    await client.send_message(6920661749, message=text)
