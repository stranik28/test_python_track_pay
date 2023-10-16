from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.payment import RequestSetPayment
from api.request.ride import RequestTouch
from api.response.ride import RideResponse, RideResponseFactory, RideHistoryResponseFactory, RideHistoryResponse
from db.models.rides import DBRide
from managers.ride import RideManager
from server.depends import get_auth_account_id, get_session, PagesPaginationParams
from vendors.exception import BluetoothNotFound, AccessDenied, RideNotFound, UserNotFound, NotSureToCreateRide, \
    RideAlreadyDone, EspNotFound

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
        datas: RequestTouch,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    for data in datas.bluetooth_mac:
        print(datas)
        try:
            ride: DBRide = await RideManager.touch(session=session, user_id=user_id, bluetooth_mac=data)
        except BluetoothNotFound:
            continue
        if ride is not None:
            return RideResponseFactory.get_from_model(ride)
    raise HTTPException(status_code=404, detail="Устойство bluetooth не найдено в базе!")


@router.get('/touch_esp/{esp_id}/{uuid}', status_code=200)
async def touch(
        uuid: str,
        esp_id: int,
        session: AsyncSession = Depends(get_session)
):
    try:
        await RideManager.esp_touch(session=session, uuid=uuid, esp_id=esp_id)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь с таким uuid не найден ")
    except NotSureToCreateRide:
        raise HTTPException(status_code=401, detail="Недостаточно пока оснований для создания поездки")
    except RideAlreadyDone:
        raise HTTPException(status_code=401, detail="Недостаточно пока оснований для создания поездки")
    except EspNotFound:
        raise HTTPException(status_code=400, detail="Не найденно доверненного устрйоства с таким id")
    print(f"Ought uuid is {uuid} from esp {esp_id}")
    return {"result": uuid}


@router.get('/touch_esp/{esp_id}/{uuid}/admin', status_code=200)
async def touch(
        uuid: str,
        esp_id: int,
        session: AsyncSession = Depends(get_session)
):
    try:
        await RideManager.esp_touch(session=session, uuid=uuid, esp_id=esp_id, admin=True)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь с таким uuid не найден ")
    except NotSureToCreateRide:
        raise HTTPException(status_code=401, detail="Недостаточно пока оснований для создания поездки")
    except RideAlreadyDone:
        raise HTTPException(status_code=401, detail="Недостаточно пока оснований для создания поездки")
    except EspNotFound:
        raise HTTPException(status_code=400, detail="Не найденно доверненного устрйоства с таким id")
    print(f"Ought uuid is {uuid} from esp {esp_id}")
    return {"result": uuid}


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
