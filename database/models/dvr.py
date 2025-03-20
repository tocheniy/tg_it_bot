from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class Dvr(Base):
    __tablename__ = "dvrs"
    name: Mapped[str] = mapped_column(String(30))
    ip: Mapped[str] = mapped_column(String(16))
    login: Mapped[str] = mapped_column(String(16))
    password: Mapped[str] = mapped_column(String(20))

    division_id: Mapped[int | None] = mapped_column(ForeignKey("divisions.id"))
    division: Mapped["Division"] = relationship(back_populates="dvrs", lazy="joined")  # type: ignore # noqa: F821

    events: Mapped[list["Event"]] = relationship(back_populates="dvr")  # type: ignore  # noqa: F821
