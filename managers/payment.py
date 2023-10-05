from sqlalchemy.ext.asyncio import AsyncSession

from db.models.rides import DBRide
from db.repository.bluetooth import BluetoothRepository
from db.repository.payment import PaymentRepository
from db.repository.ride import RideRepository
from vendors.exception import RideNotFound, PaymentAccountNotFound


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

        payment_account_id = await PaymentRepository(session).get_payment_account(user_id=user_id)

        if payment_account_id is None or payment_account_id == []:
            raise PaymentAccountNotFound

        payment_account_id = payment_account_id[0]

        await PaymentRepository(session).pay(ride_id=ride.id, account_id=payment_account_id.id, status_id=status_id,
                                             ammount=ride.transport.price)

        return status_id
