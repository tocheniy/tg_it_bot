import asyncio
import sys
from sqlalchemy import select

if __name__ == "__main__":
    sys.path.append(".")
from database.main import async_session
from database.models.dvr import Events

async_session = async_session()


async def get_all_events() -> list[Events]:
    try:
        async with async_session as session:
            stmt = select()
            res = await session.execute(stmt)
            res = res.all()
            return res
    except Exception as ex:
        print(ex)


# async def get_dvr_by_name(name: str) -> Dvr | None:
#     try:
#         async with async_session as session:
#             stmt = select(Dvr)
#             stmt = stmt.where(Dvr.name == name)
#             res = await session.execute(stmt)
#             res = res.one_or_none()
#             return res[0] if res else None

#     except Exception as ex:
#         print(ex)


async def main():
    events = await get_all_events()
    print(events)
    # dvr = await get_dvr_by_name("Reg 6 VLG")
    # print(dvr)
    # await async_session.close()


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())
