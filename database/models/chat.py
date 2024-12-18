from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base


class Chat(Base):
    __tablename__ = "chats"
    tg_chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hdd_error: Mapped[int] = mapped_column(Integer, nullable=False)
    view_tampering: Mapped[int] = mapped_column(Integer, nullable=False)
    video_signal_lost: Mapped[int] = mapped_column(Integer, nullable=False)
    cities: Mapped[list['City']] = relationship(back_populates="chat") # type: ignore # noqa: F821
