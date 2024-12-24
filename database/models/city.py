from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class City(Base):
    __tablename__ = "cities"
    short_name: Mapped[str] = mapped_column(String(30), nullable=False)
    ru_name: Mapped[str] = mapped_column(String(30), nullable=False)
    region: Mapped[str] = mapped_column(String(30), nullable=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    chat: Mapped["Chat"] = relationship(back_populates="cities")  # type: ignore # noqa: F821
