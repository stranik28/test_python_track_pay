from api.request.base import RequestBase

from pydantic import Field


class RequestSetPayment(RequestBase):
    payment_account_id: int = Field(..., examples=['12'])


class RequestPay(RequestBase):
    ride_id: int = Field(..., examples=[1,2,3])


