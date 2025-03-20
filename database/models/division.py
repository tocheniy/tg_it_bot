from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class Division(Base):
    __tablename__ = "divisions"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    city: Mapped["City"] = relationship(back_populates="division", lazy="joined")  # type: ignore  # noqa: F821
    
    chat_id: Mapped[int | None] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship(back_populates="divisions", lazy="joined")  # type: ignore  # noqa: F821

    dvrs: Mapped[list["Dvr"]] = relationship(back_populates="division")  # type: ignore # noqa: F821
    # events: Mapped[list["Event"]] = relationship(back_populates="division")  # type: ignore  # noqa: F821
