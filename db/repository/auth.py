import datetime
from typing import Optional

from sqlalchemy import select, desc, and_
from sqlalchemy.orm import joinedload

from db.models.users import DBUser
from db.models.verification_code import DBVerifyCode
from db.repository.base import BaseRepository


class AuthRepository(BaseRepository):

    async def check_phone_unique(self, phone_numb: str) -> list[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.phone_number == phone_numb
            ).limit(1)
        )

        return await self.all_ones(query)

    async def check_email_unique(self, email: str) -> list[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                and_(
                    DBUser.email == email,
                    DBUser.active == True
                )
            ).limit(1)
        )

        return await self.all_ones(query)

    async def create_user(self, first_name: str, last_name: str, middle_name: Optional[str],
                          phone_number: Optional[str], email: Optional[str], password: str) -> DBUser:
        user: DBUser = DBUser(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_number=phone_number,
            email=email,
            password=password
        )
        await self.add_model(user)

        await self.refresh_model(user)

        return user

    async def login(self, login: str) -> Optional[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.username == login
            )
        )

        return await self.one_val(query)

    async def send_code(self, account_id: int, code: int):
        db_code = DBVerifyCode(
            account_id=account_id,
            code=code,
            type_of_code=0
        )

        await self.add_model(db_code)

    async def get_by_id(self, account_id: int) -> Optional[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.id == account_id
            )
        )

        return await self.one_val(query)

    async def get_code(self, code: int) -> list[DBVerifyCode]:

        fifteen_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)

        query = (
            select(DBVerifyCode)
            .select_from(DBVerifyCode)
            .where(
                and_(
                    DBVerifyCode.code == code,
                    DBVerifyCode.used == False,
                    DBVerifyCode.created_at >= fifteen_minutes_ago
                )
            )
            .order_by(desc(DBVerifyCode.created_at))
            .limit(1)
        )

        query = query.options(
            joinedload(DBVerifyCode.account, innerjoin=True)
        )

        return await self.all_ones(query)

    async def secure_spam(self, account_id: int) -> list[DBVerifyCode]:

        fifteen_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)

        query = (
            select(DBVerifyCode)
            .select_from(DBVerifyCode)
            .where(
                and_(
                    DBVerifyCode.account_id == account_id,
                    DBVerifyCode.created_at >= fifteen_minutes_ago
                )
            )
            .order_by(desc(DBVerifyCode.created_at))
            .limit(1)
        )

        return await self.all_ones(query)

    async def check_username_unique(self, username: str):
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.username == username
            )
        )

        return await self.all_ones(query)

    async def create_user_forum(self, username: str):
        model = DBUser(
            username=username
        )

        return await self.add_model(model)
