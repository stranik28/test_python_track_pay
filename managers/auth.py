import random
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import DBUser
from db.models.verification_code import DBVerifyCode
from db.repository.auth import AuthRepository
from vendors.exception import PhoneNotUnique, EmailNotUnique, AccessDenied


class AuthManager:

    @classmethod
    async def register_user(cls, first_name: str, last_name: str, middle_name: Optional[str],
                            phone_number: Optional[str], email: Optional[str], password: str,
                            session: AsyncSession) -> DBUser:

        if AuthRepository(session).check_phone_unique(phone_numb=phone_number):
            raise PhoneNotUnique
        elif AuthRepository(session).check_email_unique(email=email):
            raise EmailNotUnique

        return await AuthRepository(session).create_user(first_name=first_name,
                                                         last_name=last_name,
                                                         middle_name=middle_name,
                                                         phone_number=phone_number,
                                                         email=email,
                                                         password=password)

    @classmethod
    async def send_code(cls, session: AsyncSession, account_id: int) -> None:
        code = random.randint(1000, 9999)
        await AuthRepository(session).send_code(account_id=account_id, code=code)

        account: DBUser = await AuthRepository(session).get_by_id(account_id=account_id)
        # send email
        print(account.email)
        print(code)

    @classmethod
    async def login(cls, session: AsyncSession, login: str, password: str):
        user: DBUser = await AuthRepository(session).login(login=login)

        if user.password == password:
            return user
        else:
            return AccessDenied

    @classmethod
    async def verify_code(cls, session: AsyncSession, account_id: int, code: int) -> bool:

        code_db: Optional[DBVerifyCode] = await AuthRepository(session).get_code(account_id=account_id)
        code_db.account.active = True
        if (code_db is not None) & (code_db.code == code):
            code_db.account.active = True
            code_db.used = True
        else:
            return False
