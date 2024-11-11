import asyncio
import logging
import sys

# from os import getenv
from typing import Any, Dict, Union
from aiogram import Bot, Dispatcher, html, F, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputMediaPhoto

from general.emun import EVENT_TYPE_THREAD
from config import setting


# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(
    token=setting.tg.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(bot=bot)


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        self.album_data: dict = {}

    def collect_album_messages(self, event: Message):
        """
        Collect messages of the same media group.
        """
        # Check if media_group_id exists in album_data
        if event.media_group_id not in self.album_data:
            # Create a new entry for the media group
            self.album_data[event.media_group_id] = {"messages": []}
        # Append the new message to the media group
        self.album_data[event.media_group_id]["messages"].append(event)
        #
        #         # Return the total number of messages in the current media group
        return len(self.album_data[event.media_group_id]["messages"])

    #
    async def __call__(self, handler, event: Message, data: Dict[str, Any]) -> Any:
        """
        Main middleware logic.
        """
        # If the event has no media_group_id, pass it to the handler immediately
        if not event.media_group_id:
            return await handler(event, data)
        # Collect messages of the same media group
        total_before = self.collect_album_messages(event)
        # Wait for a specified latency period
        await asyncio.sleep(self.latency)
        # Check the total number of messages after the latency
        total_after = len(self.album_data[event.media_group_id]["messages"])
        # If new messages were added during the latency, exit
        if total_before != total_after:
            return
        # Sort the album messages by message_id and add to data
        album_messages = self.album_data[event.media_group_id]["messages"]
        album_messages.sort(key=lambda x: x.message_id)
        data["album"] = album_messages
        # Remove the media group from tracking to free up memory
        del self.album_data[event.media_group_id]
        # Call the original event handler
        return await handler(event, data)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("chat_id_and_thread"))
async def answer_chat_id_and_thread(message: Message) -> None:
    chat_id = message.chat.id
    thread = message.message_thread_id
    text = f"Chat_id: {chat_id}\n" f"Thread: {thread}"
    await message.answer(text)


group_id = -1002456367513


# @dp.message(F.chat.type.in_({"group", "supergroup"}))
# async def listen_handler(message: Message, bot: Bot, album: list = None) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     event_type: str = ""
#     msg_list: list = []
#     # message_id = message.message_id
#     if message.text:
#         msg_list = message.text.split("\n")
#     elif album:
#         msg_list = album[0].caption.split("\n")
#     elif message.photo:
#         msg_list = message.caption.split("\n")
#     else:
#         print(
#             f"Неизвестный тип сообщения в группе {message.chat.title} от {message.from_user.full_name}"
#         )

#     event_type = [item for item in msg_list if "EVENT TYPE" in item]
#     if not event_type:
#         return
#     event_type = event_type[0].split(":")[1].strip()
#     event_type = event_type.replace(" ", "_").upper()
#     thread = EVENT_TYPE_THREAD[event_type].value

#     # msg_list = [item.replace("<", "").replace(">", "") for item in msg_list]
#     # text = " ".join(msg_list)
#     # print(text)
#     if message.text:
#         await bot.send_message(
#             chat_id=group_id,
#             text=message.text.replace("<", "").replace(">", ""),
#             message_thread_id=thread,
#         )
#     elif album:
#         msg_list = album[0].caption.split("\n")
#         medias = [InputMediaPhoto(media=message.photo[0].file_id) for message in album]
#         medias[0].caption = album[0].caption.replace("<", "").replace(">", "")
#         await bot.send_media_group(
#             chat_id=group_id,
#             media=medias,
#             message_thread_id=thread,
#         )

#     elif message.photo:
#         await bot.send_photo(
#             chat_id=group_id,
#             photo=message.photo[0].file_id,
#             caption=message.caption.replace("<", "").replace(">", ""),
#             message_thread_id=thread,
#         )
#     else:
#         print(
#             f"Неизвестный тип сообщения в группе {message.chat.title} от {message.from_user.full_name}"
#         )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    dp.message.middleware(AlbumMiddleware())
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
