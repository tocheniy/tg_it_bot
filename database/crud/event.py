# import asyncio
# from datetime import datetime
import asyncio
from datetime import datetime, timedelta
import sys
from sqlalchemy import func, select
from sqlalchemy.sql import and_
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser

if __name__ == "__main__":
    sys.path.append(".")
from database.models.chat import Chat
from database.models.division import Division
from general.schemas import EventDbSch, EventWithDvr
from database.main import async_session
from database.models.event import Event
from database.models.dvr import Dvr


async_session = async_session()


async def get_events_by_dvrname(name: str) -> list[EventWithDvr]:
    try:
        async with async_session as session:
            stmt = select(
                Event,
                Dvr.name.label("dvr_name"),
                Dvr.ip.label("ip"),
                Dvr.city.label("city"),
            ).join(Dvr, Dvr.name == name)
            res = await session.execute(stmt)
            res = res.all()
            res = [
                EventWithDvr(
                    name=item.dvr_name,
                    ip=item.ip,
                    city=item.city,
                    event=item.Event.to_dict(),
                )
                for item in res
            ]
            return res
    except Exception as ex:
        print(ex)


async def get_events_by_datetime(time: str) -> list[EventWithDvr]:
    try:
        first_time = parser.parse(time)
        last_time = first_time + timedelta(hours=23, minutes=59, seconds=59)
        async with async_session as session:
            query = select(Event, Dvr, Division)
            query = query.join(Dvr, Dvr.id == Event.dvr_id)
            query = query.join(Division, Dvr.division_id == Division.id)

            query = query.where((Event.time >= first_time) & (Event.time <= last_time))
            query = query.order_by(Event.time)

            res = await session.execute(query)
            res = res.all()
            res = [
                EventWithDvr(
                    name=dvr.name,
                    ip=dvr.ip,
                    city=division.city.ru_name,
                    event=event,
                )
                for event, dvr, division in res
            ]
            return res
    except Exception as ex:
        print(ex)


async def get_events_by_datetime_and_chat(
    time: str,
    chat_id: int,
) -> list[EventWithDvr]:
    try:
        first_time = parser.parse(time)
        last_time = first_time + timedelta(hours=24, minutes=00, seconds=00)

        async with async_session as session:
            query = select(Event, Dvr, Division, Chat)
            query = query.select_from(Event)
            query = query.join(Dvr, Dvr.id == Event.dvr_id)
            query = query.join(Division, Dvr.division_id == Division.id)
            query = query.join(Chat, Chat.id == Division.chat_id)

            query = query.where(chat_id == Chat.tg_chat_id)
            query = query.where((Event.time >= first_time) & (Event.time <= last_time))
            query = query.order_by(Event.time)

            res = await session.execute(query)
            res = res.all()
            res = [
                EventWithDvr(
                    name=dvr.name,
                    ip=dvr.ip,
                    city=division.city.ru_name,
                    event=event,
                )
                for event, dvr, division, chat in res
            ]
            return res
    except Exception as ex:
        print(ex)


async def get_events_by_city_and_datetime(city: str, time: str) -> list[EventWithDvr]:
    try:
        first_time = parser.parse(time)
        last_time = first_time + timedelta(hours=23, minutes=59, seconds=59)
        async with async_session as session:
            stmt = select(
                Event,
                Dvr.name.label("dvr_name"),
                Dvr.ip.label("ip"),
                Dvr.division.city.label("city"),
            )
            stmt = stmt.join(Dvr, Dvr.id == Event.dvr_id)
            filters = and_(
                Dvr.division.city == city,
                Event.time >= first_time,
                Event.time <= last_time,
            )
            stmt = stmt.where(filters)
            stmt = stmt.order_by(Event.time)
            res = await session.execute(stmt)
            res = res.all()
            res = [
                EventWithDvr(
                    name=item.dvr_name,
                    ip=item.ip,
                    city=item.city,
                    event=item.Event.to_dict(),
                )
                for item in res
            ]
            return res
    except Exception as ex:
        print(ex)


async def get_all_events() -> list[EventDbSch]:
    try:
        async with async_session as session:
            stmt = select(Event)
            res = await session.execute(stmt)
            res = res.scalars().all()
            res = [EventDbSch.model_validate(item) for item in res]
            return res
    except Exception as ex:
        print(ex)


async def add_event(event: EventDbSch) -> Event | None:
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


async def main():
    # events = await get_events_by_dvrname("Reg 5 VLG")
    # print(events)

    # events = await get_all_events()
    # print(events)

    events = await get_events_by_datetime("19.12.2024")
    if not events:
        return

    for ev in events[:10]:
        print(ev.event.time)
    # print(len(events))

    # print(events[0])
    # print(events[-1])

    # # events = await get_events_by_city_and_datetime("MSK", "15.12.2024")
    # print(len(events))
    # print(events[0])
    # print(events[-1])


#     ev = EventModel(
#         # id=1,
#         name="dasdasda",
#         dvr_id=1,
#         time=datetime.now(),
#     )
#     # print(ev)
#     event = await add_event(ev)
#     print(event)
#     # dvr = await get_dvr_by_name("Reg 6 VLG")
#     # print(dvr)
#     # await async_session.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
#     asyncio.run(main())
