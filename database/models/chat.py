from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main import Base
from database.models.division import Division


class Chat(Base):
    __tablename__ = "chats"
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    hdd_error: Mapped[int] = mapped_column(Integer, nullable=False)
    view_tampering: Mapped[int] = mapped_column(Integer, nullable=False)
    video_signal_lost: Mapped[int] = mapped_column(Integer, nullable=False)
    divisions: Mapped[list["Division"]] = relationship(back_populates="chat")
