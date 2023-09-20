from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm

from api.request.auth import RequestRegistration, RequestEmailCode, ChangePassword, RequestEmailCodeVerify
from server.depends import get_session

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post('/register_user', summary="Регистрация пользователя", deprecated=True)
async def register_user(
        registration_data: RequestRegistration,
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/send_verification_code', summary="Отправить код для верификации e-mail", deprecated=True)
async def verification_code(
        email: RequestEmailCode,
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/verify_code', summary="Верифицкация кода от e-mail", deprecated=True)
async def verifycation_code_verify(
        verification_data: RequestEmailCodeVerify,
        session: AsyncSession = Depends(get_session)
):
    pass


@router.post('/login', summary="Логин", deprecated=True)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    pass


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
