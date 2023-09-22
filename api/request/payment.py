from api.request.base import RequestBase

from pydantic import Field


class RequestSetPayment(RequestBase):
    payment_account: str = Field(..., examples=['4377731278883770'])


class RequestPay(RequestBase):
    bluetooth_devise_id: int = Field(..., examples=['123124'])


