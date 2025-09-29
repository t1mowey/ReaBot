from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf import get_db
from app.repositories import get_user_by_t_id
from app.schema import UserOut
from app.registration.services import check_and_add_user

router = APIRouter()


@router.get("/users/get", response_model=UserOut)
async def get_user_by_tid(t_id: int,
                          db: AsyncSession = Depends(get_db)) -> UserOut:
    user = await get_user_by_t_id(db, t_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/users/register", response_model=UserOut)
async def register_user(user_id: int,
                        db: AsyncSession = Depends(get_db)):
    try:
        resp = await check_and_add_user(db, user_id)
    except BaseException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Try")
    return resp
    ...