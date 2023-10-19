from typing import Optional

from api.response.base import ResponseBase
from pydantic import Field
from datetime import datetime

from db.models.ride_status import DBRideStatus
from db.models.rides import DBRide


class RideStatusResponse(ResponseBase):
    id: int = Field(...)
    name: str = Field(...)


class RideStatusFactory:

    @staticmethod
    def get_from_model(model: DBRideStatus) -> RideStatusResponse:
        return RideStatusResponse(
            id=model.id,
            name=model.name
        )


class RideResponse(ResponseBase):
    id: int = Field(...)
    name: str = Field(...)
    start_time: Optional[datetime] = Field(None)
    start_place: Optional[str] = Field(None)
    end_time: Optional[datetime] = Field(None)
    end_place: Optional[str] = Field(None)
    route_numb: str = Field(...)
    price: int = Field(...)
    payment_method: str = Field(...)
    licence_plate: str = Field(...)
    status_id: int = Field(...)
    qr: str = Field(...)


class RideHistoryResponse(ResponseBase):
    id: int = Field(...)
    ride_name: str = Field(...)
    price: int = Field(...)
    time: datetime = Field(...)
    status: str = Field(...)


class RideResponseFactory:

    @staticmethod
    def get_from_model(model: DBRide) -> RideResponse:
        return RideResponse(
            id=model.id,
            name=model.ride_name,
            start_time=model.created_at,
            route_numb=model.transport.route_numb,
            price=model.transport.price,
            payment_method="СБП",
            licence_plate=str(model.transport.number + model.transport.region_numb),
            status_id=model.status.id,
            qr="https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg"
        )


class RideHistoryResponseFactory:

    @staticmethod
    def get_from_model(ride: DBRide) -> RideHistoryResponse:
        return RideHistoryResponse(
            id=ride.id,
            time=ride.created_at,
            price=ride.transport.price,
            status=ride.status.name,
            ride_name=ride.transport.type.name + " " + ride.transport.route_numb
        )

    @classmethod
    def get_from_models(cls, rides: list[DBRide]) -> list[RideHistoryResponse]:
        return [cls.get_from_model(ride) for ride in rides]
