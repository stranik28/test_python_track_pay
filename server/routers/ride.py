from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment
from api.request.ride import RequestTouch
from api.response.ride import RideResponse, RideResponseFactory, RideHistoryResponseFactory, RideHistoryResponse
from db.models.rides import DBRide
from managers.ride import RideManager
from server.depends import get_auth_account_id, get_session, PagesPaginationParams
from vendors.exception import BluetoothNotFound, AccessDenied, RideNotFound

router = APIRouter(prefix="/ride", tags=['Ride'])


@router.get('/history', response_model=list[RideHistoryResponse])
async def get_rides_history(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session),
        pagination: PagesPaginationParams = Depends()
):
    rides: list[DBRide] = await RideManager.ride_history(session=session,
                                                         user_id=user_id,
                                                         limit=pagination.limit,
                                                         offset=pagination.offset)
    return RideHistoryResponseFactory.get_from_models(rides)


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


@router.get('/{ride_id}', response_model=RideResponse)
async def get_ride(
        ride_id: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    try:
        ride: DBRide = await RideManager.get_ride(session=session, user_id=user_id, ride_id=ride_id)
    except AccessDenied:
        raise HTTPException(status_code=403, detail="У вас нет доступа к этой поездке")
    except RideNotFound:
        raise HTTPException(status_code=404, detail='Поездка не найдена')

    return RideResponseFactory.get_from_model(ride)
