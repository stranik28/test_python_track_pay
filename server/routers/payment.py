from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment, RequestPay
from managers.payment import PaymentManager
from managers.ride import RideManager
from server.depends import get_auth_account_id, get_session
from vendors.exception import RideNotFound, PaymentAccountNotFound, DeleteMainPaymentMethod, EspNotFound

router = APIRouter(prefix="/payment", tags=['Payment'])


@router.get('/', response_model=list[int])
async def get_my_payments(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    await PaymentManager.get_payments_methods(session=session, user_id=user_id)


@router.patch('/set_new_payment', status_code=204)
async def set_payment(
        new_payment_main: RequestSetPayment,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    await PaymentManager.set_payment(session=session,
                                     user_id=user_id,
                                     payment_account=new_payment_main.payment_account_id)


@router.post('/add_new_payment', status_code=202)
async def add_new_payment(
        sbp_account: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    await PaymentManager.add_new(sbp_account=sbp_account, user_id=user_id, session=session)


@router.delete('/delete_payment/{payment_id}', status_code=200)
async def delete_payment(
        payment_id: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    try:
        await PaymentManager.delete(payment_id=payment_id, user_id=user_id, session=session)
    except DeleteMainPaymentMethod:
        raise HTTPException(status_code=401, detail="Нельзя удалить основной способ оплаты")
    except PaymentAccountNotFound:
        raise HTTPException(status_code=404, detail="Платежный аккаунт не найдет")


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

    except EspNotFound:
        raise HTTPException(status_code=404, detail="Для оплаты проезда снчала выберете основной способ оплаты")

    await RideManager.change_status(session=session, status_id=2, ride_id=ride_info.ride_id)
