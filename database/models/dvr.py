from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class Dvr(Base):
    __tablename__ = "dvrs"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    ip: Mapped[str] = mapped_column(String(16), nullable=False)
    login: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    
    events: Mapped[list["Event"]] = relationship(back_populates="dvr")  # type: ignore  # noqa: F821
    city_tmp: Mapped["City"] = relationship(back_populates="dvrs")  # type: ignore  # noqa: F821
