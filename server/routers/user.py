from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.user import RequestUserUpdate, RequestUserLimitRides
from server.depends import get_auth_account_id, get_session

router = APIRouter(prefix="/user", tags=['User'])


@router.get('/', deprecated=True)
async def get_user_profile(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


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
