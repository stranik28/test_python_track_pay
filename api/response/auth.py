from api.response.base import ResponseBase
from db.models.users import DBUser
from server.depends import get_access_token


class ResponseUser(ResponseBase):
    user_id: int
    access_token: str


class ResponseAuthFactory:

    @staticmethod
    def get_user(user: DBUser) -> ResponseUser:
        return ResponseUser(user_id=user.id, access_token=get_access_token(user))


    @staticmethod
    def get_user_android(user: DBUser) -> ResponseUser:
        return ResponseUser(user_id=user.id, access_token=str('Bearer ' + get_access_token(user)))
