from api.request.base import RequestBase

from pydantic import Field


class RequestSetPayment(RequestBase):
    ride_id: int = Field(..., examples=['176'])
    dispute_text: str = Field(..., examples=['Я спал в это время'])