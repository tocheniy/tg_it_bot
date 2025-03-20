from datetime import datetime
from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base
# from database.models.division import Division


class Event(Base):
    __tablename__ = "events"
    name: Mapped[str] = mapped_column(String(30))

    dvr_id: Mapped[int] = mapped_column(ForeignKey("dvrs.id"))
    dvr: Mapped["Dvr"] = relationship(back_populates="events")  # type: ignore # noqa: F821

    camera: Mapped[str | None] = mapped_column(String(30))
    time: Mapped[datetime] = mapped_column(DateTime)

    # division_id = Mapped[int] = mapped_column(ForeignKey("divisions.id"), nullable=True)
    # division: Mapped["Division"] = relationship(back_populates="events")
