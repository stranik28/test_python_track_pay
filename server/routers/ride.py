from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment
from server.depends import get_auth_account_id, get_session, PagesPaginationParams

router = APIRouter(prefix="/ride", tags=['Ride'])


@router.get('/history', deprecated=True)
async def get_rides_history(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session),
        pagination: PagesPaginationParams = Depends()
):
    pass


@router.get('/curent_ride', deprecated=True)
async def get_ride(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.get("/ride_recipe/{ride_id}", deprecated=True)
async def get_recipe(
        ride_id: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


# TODO сделать в модельках
@router.post("/ride_dispute", deprecated=True)
async def get_recipe(
        dispute_form: RequestSetPayment,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass
