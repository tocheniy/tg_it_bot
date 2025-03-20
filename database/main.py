from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from config import setting


class Base(DeclarativeBase):
    """Base"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self) -> str:
        # * Получаем имена и значения всех столбцов для текущего экземпляра
        fields = ", ".join(
            f"{column.name}={getattr(self, column.name)!r}"
            for column in inspect(self.__class__).c
        )
        # *  Возвращаем строку представления с именем класса и полями
        return f"{self.__class__.__name__}({fields})"


engine: AsyncEngine = create_async_engine(url=setting.db.url(), echo=setting.db.echo)
async_session: AsyncSession = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
