import random
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import DBUser
from db.models.verification_code import DBVerifyCode
from db.repository.auth import AuthRepository
from vendors.exception import PhoneNotUnique, EmailNotUnique, AccessDenied, CodeNotValid, SpamError, UsernameNotUnique

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from configs.config import SMTP_USER, SMTP_PORT, SMTP_PASS, SMTP_SERVER


class AuthManager:

    @staticmethod
    async def send_code_to_email(to: str, link: str):
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to
        msg['Subject'] = 'Ссылка для подтверждения регистрации "Плати в Пути"'

        message = f'Ваша ссылка для подтверждения регистрации: {link}'
        msg.attach(MIMEText(message))

        smtp_connection = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_connection.starttls()
        smtp_connection.login(SMTP_USER, SMTP_PASS)
        smtp_connection.sendmail(
            SMTP_USER, to, msg.as_string())
        smtp_connection.quit()

    @classmethod
    async def register_user(cls, first_name: str, last_name: str, middle_name: Optional[str],
                            phone_number: Optional[str], email: Optional[str], password: str,
                            session: AsyncSession) -> DBUser:

        if await AuthRepository(session).check_phone_unique(phone_numb=phone_number):
            raise PhoneNotUnique

        elif await AuthRepository(session).check_email_unique(email=email):
            raise EmailNotUnique

        return await AuthRepository(session).create_user(first_name=first_name,
                                                         last_name=last_name,
                                                         middle_name=middle_name,
                                                         phone_number=phone_number,
                                                         email=email,
                                                         password=password)

    @classmethod
    async def send_code(cls, session: AsyncSession, account_id: int) -> None:
        code = random.randint(0, 2000000)

        account: DBUser = await AuthRepository(session).get_by_id(account_id=account_id)

        link = f'http://185.192.246.110:8000/auth/verify/{code}'

        if len(await AuthRepository(session).secure_spam(account_id)) > 0:

            raise SpamError

        await cls.send_code_to_email(to=account.email, link=link)

        await AuthRepository(session).send_code(account_id=account_id, code=code)

    @classmethod
    async def login(cls, session: AsyncSession, login: str, password: str):
        user: list[DBUser] = await AuthRepository(session).login(login=login)
        if user == []:
            user: DBUser = await cls.register_user_forum(session=session, username=login)
        else:
            user = user[0]

        # if user.password == password:
        return user
        # else:
        #     return AccessDenied

    @classmethod
    async def verify_code(cls, session: AsyncSession, code: int) -> None:

        code_db: list[DBVerifyCode] = await AuthRepository(session).get_code(code=code)
        if code_db == [] or code_db is None:
            raise CodeNotValid

        code_db = code_db[0]

        code_db.account.active = True
        code_db.used = True

        await session.commit()

    @staticmethod
    async def register_user_forum(session: AsyncSession, username: str):
        if await AuthRepository(session).check_username_unique(username=username):
            raise UsernameNotUnique
        return await AuthRepository(session).create_user_forum(username=username)

