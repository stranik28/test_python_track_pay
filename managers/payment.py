from sqlalchemy.ext.asyncio import AsyncSession

from db.models.rides import DBRide
from db.models.sbp_accounts import DBUserSBPAccount
from db.repository.bluetooth import BluetoothRepository
from db.repository.payment import PaymentRepository
from db.repository.ride import RideRepository
from vendors.exception import RideNotFound, PaymentAccountNotFound, DeleteMainPaymentMethod


class PaymentManager:

    @staticmethod
    async def pay(session: AsyncSession, user_id: int, ride_id: int) -> int:

        ride: list[DBRide] = await RideRepository(session).get_by_id(ride_id)

        if ride is None or ride == []:
            raise RideNotFound
        else:
            ride = ride[0]

        # Payment logic

        status_id = 2

        # payment_account_id = await PaymentRepository(session).get_payment_account(user_id=user_id)

        # if payment_account_id is None or payment_account_id == []:
        #     raise PaymentAccountNotFound

        # payment_account_id = payment_account_id[0]

        await PaymentRepository(session).pay(ride_id=ride.id, account_id=None, status_id=status_id,
                                             ammount=ride.transport.price)

        return status_id

    @classmethod
    async def add_new(cls, sbp_account: int, user_id: int, session: AsyncSession):

        account = await PaymentRepository(session).add_payment(user_id=user_id, sbp_account=sbp_account)

        main_account = await PaymentRepository(session).get_payment_account(user_id)

        if main_account == [] or main_account is None:
            await PaymentRepository(session).create_new_payment_main(user_id=user_id, payment_account=account.id)

    @classmethod
    async def delete(cls, payment_id: int, user_id: int, session: AsyncSession):

        main_account = await PaymentRepository(session).get_payment_account(user_id)

        if main_account:
            main_account = main_account[0]
            if main_account.account_id == payment_id:
                raise DeleteMainPaymentMethod

        account = await PaymentRepository(session).get_by_sbp_account(user_id=user_id, payment_id=payment_id)

        if account == [] or account is None:
            raise PaymentAccountNotFound

        account = account[0]

        await PaymentRepository(session).delete(account)

    @staticmethod
    async def set_payment(session: AsyncSession, user_id: int, payment_account: int):

        main_account: list[DBUserSBPAccount] = await PaymentRepository(session).get_payment_account(user_id)

        if main_account == [] or main_account is None:
            await PaymentRepository(session).create_new_payment_main(user_id=user_id, payment_account=payment_account)
        else:
            main_account = main_account[0]
            main_account.account_id = payment_account
            main_account.user_id = user_id

            await session.commit()

    @staticmethod
    async def get_payments_methods(session: AsyncSession, user_id: int) -> list[DBUserSBPAccount]:
        main_account: list[DBUserSBPAccount] = await PaymentRepository(session).get_payment_account(user_id)
        if main_account == [] or main_account is None:
            return []
        main_account = main_account[0]
        payments = await PaymentRepository(session).get_payments_account(user_id=user_id)

        for payment in payments:
            if main_account.id == payment.id:
                payment.ride_primary = True

        return payments

    @staticmethod
    async def set_paymenst(session, user_id, devise_token, devise_uuid):

        exist = await BluetoothRepository(session).get_notification_by_id(user_id)

        if exist == []:
            await BluetoothRepository(session).set_new_notification_info(user_id=user_id, devise_token=devise_token, devise_uuid=devise_uuid)
            return
        exist = exist[0]

        exist.token = devise_token
        exist.uuid = devise_uuid
        print(devise_uuid)
        print(devise_token)
        await session.commit()
        return
