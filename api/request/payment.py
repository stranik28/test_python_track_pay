from api.request.base import RequestBase

from pydantic import Field


class RequestSetPayment(RequestBase):
    payment_account: str = Field(..., examples=['4377731278883770'])