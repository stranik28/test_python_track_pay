from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm

from api.request.auth import RequestRegistration, RequestEmailCode, ChangePassword, RequestEmailCodeVerify
from api.response.auth import ResponseUserFactory, ResponseUser
from db.models.users import DBUser
from managers.auth import AuthManager
from server.depends import get_session, get_auth_account_id_unverified

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post('/register_user', summary="Регистрация пользователя", response_model=ResponseUser)
async def register_user(
        registration_data: RequestRegistration,
        session: AsyncSession = Depends(get_session)
):
    user: DBUser = await AuthManager.register_user(session=session, first_name=registration_data.first_name,
                                                   last_name=registration_data.last_name,
                                                   middle_name=registration_data.middle_name,
                                                   phone_number=registration_data.phone_number,
                                                   email=registration_data.email,
                                                   password=registration_data.password)
    return ResponseUserFactory.get_user(user=user)


@router.post('/send_verification_code', summary="Отправить код для верификации e-mail", description="Отправка кода пока не работает, а так ручка рабочая ")
async def verification_code(
        account_id: int = Depends(get_auth_account_id_unverified),
        session: AsyncSession = Depends(get_session)
):
    await AuthManager.send_code(session=session, account_id=account_id)


@router.post('/verify_code', summary="Верифицкация кода от e-mail", description="Пока всегда Тру")
async def verifycation_code_verify(
        verification_data: RequestEmailCodeVerify,
        account_id: int = Depends(get_auth_account_id_unverified),
        session: AsyncSession = Depends(get_session)
):
    return await AuthManager.verify_code(session=session, account_id=account_id, code=verification_data.code)


@router.post('/login', summary="Логин")
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user = await AuthManager.login(session=session, login=form_data.username, password=form_data.password)

    return ResponseUserFactory.get_user(user=user)


@router.post('/send_recovery_code', summary="Отправка кода для смены пароля", deprecated=True)
async def recovery(
        email: RequestEmailCode,
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/change_password', summary="Смена пароля с кодом от e-mail", deprecated=True)
async def verify_recover_code(
        change_form: ChangePassword,
        session: AsyncSession = Depends(get_session)
):
    pass
