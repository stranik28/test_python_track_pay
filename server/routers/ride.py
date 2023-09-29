from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment
from api.request.ride import RequestTouch
from api.response.ride import RideResponse, RideResponseFactory
from db.models.rides import DBRide
from managers.ride import RideManager
from server.depends import get_auth_account_id, get_session, PagesPaginationParams
from vendors.exception import BluetoothNotFound

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


@router.post('/touch', response_model=RideResponse)
async def touch(
        data: RequestTouch,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    try:
        ride: DBRide = await RideManager.touch(session=session, user_id=user_id, bluetooth_mac=data.bluetooth_mac)
    except BluetoothNotFound:
        raise HTTPException(status_code=404, detail="Устойство bluetooth не найдено в базе!")

    return RideResponseFactory.get_from_model(ride)
