from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserCalendar, User


async def update_google_token(db: AsyncSession, user_id: int, refresh_token: str, provider: str = "google_calendar"):
    stmt = select(UserCalendar).where(UserCalendar.user_id==user_id)
    res = await db.execute(stmt)
    exist = res.scalar_one_or_none()
    # stmt = select(User).where(User.t_id == user_id)
    # res = await db.execute(stmt)
    # user = res.scalar_one_or_none()
    if exist:
        exist.refresh = refresh_token
        exist.provider = provider
        await db.commit()
        await db.refresh(exist)
        return exist
    else:
        new_user_calendar = UserCalendar(user_id=user_id, refresh=refresh_token, provider=provider)
        db.add(new_user_calendar)
        await db.commit()
        await db.refresh(new_user_calendar)
        return new_user_calendar


async def get_user_by_id(db: AsyncSession, user_id: int):
    res = await db.get(User, user_id)
    return res


async def get_user_by_t_id(db: AsyncSession, t_id: int):
    res = await db.execute(
        select(User).where(User.t_id == t_id)
    )
    user = res.scalar_one_or_none()
    return user


async def check_user(db: AsyncSession, t_id: int) -> User:
    res = await db.execute(
        select(User).where(User.t_id==t_id)
    )
    return res.scalar_one_or_none()


async def register_user(db: AsyncSession, t_id: int) -> User:
    new_user = User(t_id=t_id)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
