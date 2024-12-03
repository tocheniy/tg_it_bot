from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.main import Base


class Dvr(Base):
    __tablename__ = "dvrs"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    ip: Mapped[str] = mapped_column(String(16), nullable=False)
    login: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    city: Mapped[str] = mapped_column(String(20), nullable=False)
