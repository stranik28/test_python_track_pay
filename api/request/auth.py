from typing import Optional

from api.request.base import RequestBase

from pydantic import Field


class RequestRegistration(RequestBase):
    first_name: str = Field(..., examples=["Александр"])
    last_name: str = Field(..., examples=["Бородач"])
    middle_name: Optional[str] = Field(None, examples=['Родионович'])

    phone_number: Optional[str] = Field(None, examples=['+74753149599'])
    email: Optional[str] = Field(None, examples=['nikita@trackpay.com'])

    password: str = Field(..., examples=['123'])


class RequestLogin(RequestBase):
    username: str = Field(..., examples=['your_email@gmail.com'])
    password: str = Field(..., examples=['your_password'])


class RequestEmailCode(RequestBase):
    email: str = Field(..., examples=['your_email@gmail.com'])


class RequestEmailCodeVerify(RequestBase):
    email: str = Field(..., examples=['your_email@gmail.com'])
    code: str = Field(..., examples=['123456'])


class ChangePassword(RequestBase):
    email: str = Field(..., examples=['your_email@gmail.com'])
    code: str = Field(..., examples=['123456'])
    password: str = Field(..., examples=['your_password'])
