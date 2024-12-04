import asyncio
from datetime import datetime
import sys
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

if __name__ == "__main__":
    sys.path.append(".")
from general.schemas import EventModel
from database.main import async_session
from database.models.event import Event


async_session = async_session()


async def get_all_events() -> list[Event]:
    try:
        async with async_session as session:
            stmt = select()
            res = await session.execute(stmt)
            res = res.all()
            return res
    except Exception as ex:
        print(ex)


async def add_event(event: EventModel) -> Event | None:
    async with async_session as session:
        event = event.model_dump(exclude_none=True)
        data = Event(**event)
        session.add(data)
        try:
            await session.commit()
        except SQLAlchemyError as ex:
            await session.rollback()
            raise ex
        return data
        # res = await session.execute(stmt)
        # res = res.all()
        # return res


async def main():
    # events = await get_all_events()
    # print(events)
    ev = EventModel(
        # id=1,
        name="dasdasda",
        dvr_id=1,
        time=datetime.now(),
    )
    # print(ev)
    event = await add_event(ev)
    print(event)
    # dvr = await get_dvr_by_name("Reg 6 VLG")
    # print(dvr)
    # await async_session.close()


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())
