import asyncio
import sys
from sqlalchemy import select


if __name__ == "__main__":
    sys.path.append(".")
from database.main import async_session
from database.models.chat import Chat

async_session = async_session()


async def get_chats() -> list[Chat]:
    try:
        async with async_session as session:
            query = select(Chat)
            res = await session.execute(query)
            res = [item[0] for item in res.all()]
            return res
    except Exception as ex:
        print(ex)


async def main():
    items = await get_chats()
    if not items:
        return
    print(items)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
