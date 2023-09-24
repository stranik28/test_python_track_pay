from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.user import RequestUserUpdate, RequestUserLimitRides
from api.response.user import ResponseUserFactory
from managers.user import UserManager
from server.depends import get_auth_account_id, get_session

from db.models.users import DBUser

router = APIRouter(prefix="/user", tags=['User'])


@router.get('/')
async def get_user_profile(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    user: DBUser = await UserManager.get_user(session=session, user_id=user_id)

    return ResponseUserFactory.get_from_model(user)


@router.patch('/', deprecated=True)
async def update_user_profile(
        data_to_update: RequestUserUpdate,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.patch('/set_rides_limit', deprecated=True)
async def update_user_profile(
        limit_rides: RequestUserLimitRides,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass
