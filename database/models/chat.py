from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base
from database.models.division import Division


class Chat(Base):
    __tablename__ = "chats"
    name: Mapped[str | None] = mapped_column(String(30))
    tg_chat_id: Mapped[int] = mapped_column(BigInteger)
    hdd_error: Mapped[int] = mapped_column(Integer)
    view_tampering: Mapped[int] = mapped_column(Integer)
    video_signal_lost: Mapped[int] = mapped_column(Integer)
    statistic: Mapped[int | None] = mapped_column(Integer)
    divisions: Mapped[list["Division"]] = relationship(back_populates="chat")
