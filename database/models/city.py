from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class City(Base):
    __tablename__ = "cities"
    short_name: Mapped[str] = mapped_column(String(30))
    ru_name: Mapped[str] = mapped_column(String(30))
    region: Mapped[str | None] = mapped_column(String(30))
    division: Mapped[list["Division"]] = relationship(back_populates="city")  # type: ignore # noqa: F821
