from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import check_user, register_user


async def check_and_add_user(db: AsyncSession, user_id: int):
    exist = await check_user(db, user_id)
    if exist:
        return exist
    user = await register_user(db, user_id)
    return user