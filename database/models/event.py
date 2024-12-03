from datetime import datetime
from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class Event(Base):
    __tablename__ = "events"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    dvr_id: Mapped[int] = mapped_column(ForeignKey("dvrs.id"), nullable=False)
    camera: Mapped[str] = mapped_column(String(30), nullable=True)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    dvr: Mapped["Dvr"] = relationship(back_populates="events")  # type: ignore # noqa: F821
