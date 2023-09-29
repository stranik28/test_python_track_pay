from typing import Optional

from api.response.base import BaseModel
from pydantic import Field
from datetime import datetime

from db.models.ride_status import DBRideStatus
from db.models.rides import DBRide


class RideStatusResponse(BaseModel):
    id: int = Field(...)
    name: str = Field(...)


class RideStatusFactory:

    @staticmethod
    def get_from_model(model: DBRideStatus) -> RideStatusResponse:

        return RideStatusResponse(
            id=model.id,
            name=model.name
        )


class RideResponse(BaseModel):
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
    status: RideStatusResponse = Field(...)
    qr: str = Field(...)


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
            status=RideStatusFactory.get_from_model(model.status),
            qr="https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg"
        )
