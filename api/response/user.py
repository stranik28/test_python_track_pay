from typing import Optional

from api.response.base import ResponseBase

from pydantic import Field

from db.models.users import DBUser


class ResponseUser(ResponseBase):
    id: int = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    middle_name: Optional[str] = Field(None)

    phone_number: Optional[str] = Field(None)
    email: str = Field(...)


class ResponseUserFactory:

    @staticmethod
    def get_from_model(user: DBUser) -> ResponseUser:
        return ResponseUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            phone_number=user.phone_number,
            email=user.email
        )
