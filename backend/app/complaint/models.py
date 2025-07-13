from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text
from datetime import datetime, UTC


class Base(DeclarativeBase):
    pass

class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="open")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    sentiment: Mapped[str] = mapped_column(String(10), default="unknown")
    category: Mapped[str] = mapped_column(String(20), default="другое")
    ip_country: Mapped[str] = mapped_column(String(15), nullable=True)