from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.request.auth import RequestRegistration, RequestEmailCode, ChangePassword, RequestRegistrationForum, \
    RequestLogin
from api.request.payment import RequestNotification
from api.response.auth import ResponseAuthFactory, ResponseUser

from db.models.users import DBUser

from managers.auth import AuthManager
from managers.payment import PaymentManager

from server.depends import get_session, get_auth_account_id_unverified

from vendors.exception import EmailNotUnique, PhoneNotUnique, AccessDenied, SpamError, UsernameNotUnique

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post('/register_user', summary="Регистрация пользователя", response_model=ResponseUser)
async def register_user(
        registration_data: RequestRegistrationForum,
        devise_info: Optional[RequestNotification] = None,
        session: AsyncSession = Depends(get_session)
):
    try:
        # user: DBUser = await AuthManager.register_user(session=session, first_name=registration_data.first_name,
        #                                                last_name=registration_data.last_name,
        #                                                middle_name=registration_data.middle_name,
        #                                                phone_number=registration_data.phone_number,
        #                                                email=registration_data.email,
        #                                                password=registration_data.password)
        user: DBUser = await AuthManager.register_user_forum(session=session, username=registration_data.username)
        if devise_info:
            await PaymentManager.set_paymenst(session=session, user_id=user.id,
                                              devise_token=devise_info.devise_token,
                                              devise_uuid=devise_info.devise_uuid)
    except PhoneNotUnique:
        raise HTTPException(status_code=422, detail='Такой номер телефона уже зарегистрирован')
    except EmailNotUnique:
        raise HTTPException(status_code=422, detail='Такой email уже зарегистрирован')
    except UsernameNotUnique:
        raise HTTPException(status_code=422, detail='Такой username уже зарегистрирован')

    return ResponseAuthFactory.get_user(user=user)


@router.post('/register_user', summary="Регистрация пользователя", response_model=ResponseUser)
async def register_user(
        registration_data: RequestRegistrationForum,
        devise_info: Optional[RequestNotification] = None,
        session: AsyncSession = Depends(get_session)
):
    try:
        # user: DBUser = await AuthManager.register_user(session=session, first_name=registration_data.first_name,
        #                                                last_name=registration_data.last_name,
        #                                                middle_name=registration_data.middle_name,
        #                                                phone_number=registration_data.phone_number,
        #                                                email=registration_data.email,
        #                                                password=registration_data.password)
        user: DBUser = await AuthManager.register_user_forum(session=session, username=registration_data.username)
        if devise_info:
            await PaymentManager.set_paymenst(session=session, user_id=user.id,
                                              devise_token=devise_info.devise_token,
                                              devise_uuid=devise_info.devise_uuid)
    except PhoneNotUnique:
        raise HTTPException(status_code=422, detail='Такой номер телефона уже зарегистрирован')
    except EmailNotUnique:
        raise HTTPException(status_code=422, detail='Такой email уже зарегистрирован')
    except UsernameNotUnique:
        raise HTTPException(status_code=422, detail='Такой username уже зарегистрирован')

    return ResponseAuthFactory.get_user(user=user)


@router.post('/send_verification_code')
async def verification_code(
        account_id: int = Depends(get_auth_account_id_unverified),
        session: AsyncSession = Depends(get_session)
):
    try:
        await AuthManager.send_code(session=session, account_id=account_id)
    except SpamError:
        raise HTTPException(status_code=403, detail="Оправлять сообщения на 1 почту можно не чаще 1 раза в 15 минут")


@router.get('/verify/{verification_data}')
async def verifycation_code_verify(
        verification_data: int,
        session: AsyncSession = Depends(get_session)
):
    await AuthManager.verify_code(session=session, code=verification_data)
    # HTML-разметка для ответа
    html_content = '''
    <html>
    <head>
        <title>Результат верификации</title>
    </head>
    <body>
        <h1>Спасибо за регистрацию, можете пользоваться приложением</h1>
    </body>
    </html>
    '''

    return HTMLResponse(content=html_content)


@router.post('/login', summary="Логин")
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    try:
        user = await AuthManager.login(session=session, login=form_data.username, password=form_data.password)
        if devise_info:
            await PaymentManager.set_paymenst(session=session, user_id=user.id,
                                              devise_token=devise_info.devise_token,
                                              devise_uuid=devise_info.devise_uuid)
    except AccessDenied:
        raise HTTPException(status_code=401, detail='Не правильный логин или пароль')

    return ResponseAuthFactory.get_user(user=user)


@router.post('/login_android', summary="Логин")
async def login_user(
        form_data: RequestLogin,
        devise_info: Optional[RequestNotification] = None,
        session: AsyncSession = Depends(get_session)
):
    try:
        user = await AuthManager.login(session=session, login=form_data.username, password=form_data.password)
        if devise_info:
            await PaymentManager.set_paymenst(session=session, user_id=user.id,
                                              devise_token=devise_info.devise_token,
                                              devise_uuid=devise_info.devise_uuid)
    except AccessDenied:
        raise HTTPException(status_code=401, detail='Не правильный логин или пароль')

    return ResponseAuthFactory.get_user_android(user=user)


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
