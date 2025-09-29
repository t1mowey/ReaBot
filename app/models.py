import asyncio
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.conf import Base, engine


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    t_id: Mapped[int] = mapped_column()



class UserCalendar(Base, TimestampMixin):
    __tablename__ = "user_calendars"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    provider: Mapped[str] = mapped_column(nullable=False)
    refresh: Mapped[str] = mapped_column(unique=True, nullable=False)



async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())


