from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment, RequestPay
from managers.payment import PaymentManager
from managers.ride import RideManager
from server.depends import get_auth_account_id, get_session
from vendors.exception import RideNotFound, PaymentAccountNotFound

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


@router.post('/pay', status_code=200)
async def pay(
        ride_info: RequestPay,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    try:
        await PaymentManager.pay(session=session, user_id=user_id, ride_id=ride_info.ride_id)

    except RideNotFound:
        raise HTTPException(status_code=404, detail="Поездка не найдена")

    except PaymentAccountNotFound:
        raise HTTPException(status_code=404, detail="Для оплаты проезда снчала выберете основной способ оплаты")

    await RideManager.change_status(session=session, status_id=2, ride_id=ride_info.ride_id)
