from typing import Optional

from api.request.base import RequestBase

from pydantic import Field


class RequestUserUpdate(RequestBase):
    first_name: Optional[str] = Field(..., examples=["Александр"])
    last_name: Optional[str] = Field(..., examples=["Бородач"])
    middle_name: Optional[str] = Field(None, examples=['Родионович'])

    phone_number: Optional[str] = Field(None, examples=['+74753149599'])
    email: Optional[str] = Field(None, examples=['nikita@trackpay.com'])

    password: Optional[str] = Field(..., examples=['123'])


class RequestUserLimitRides(RequestBase):
    limit_rides: int = Field(..., examples=[1,2,3,4,5,99])