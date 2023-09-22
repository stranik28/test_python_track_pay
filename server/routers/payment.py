from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment, RequestPay
from server.depends import get_auth_account_id, get_session

router = APIRouter(prefix="/payment", tags=['Payment'])


@router.get('/', deprecated=True)
async def get_my_payments(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.patch('/set_new_payment', deprecated=True)
async def set_payment(
        new_payment_main: RequestSetPayment,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/add_new_payment', summary="Пока не знаю как будет выгядеть", deprecated=True)
async def add_new_payment(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.delete('/delete_payment', deprecated=True)
async def delete_payment(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/pay', deprecated=True)
async def pay(
        ride_info: RequestPay,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    pass