from sqlalchemy.ext.asyncio import AsyncSession

from db.models.rides import DBRide
from db.repository.bluetooth import BluetoothRepository
from db.repository.payment import PaymentRepository
from db.repository.ride import RideRepository


class PaymentManager:

    @staticmethod
    async def pay(session: AsyncSession, user_id: int, bluetooth_devise_id: int) -> int:

        bluetooth_devise = await BluetoothRepository(session).get_by_id(bluetooth_id=bluetooth_devise_id)

        ride: DBRide = await RideRepository(session).get_ride(user_id, bluetooth_devise.transport_id)

        if ride is None or ride == []:
            ride: DBRide = await RideRepository(session).create_ride(user_id=user_id,
                                                                     transport_id=bluetooth_devise.transport_id)
        else:
            ride = ride[0]

        # Payment logic

        status_id = 2

        payment_account_id = await PaymentRepository(session).get_payment_account(user_id=user_id)

        if payment_account_id is None or payment_account_id == []:
            raise ValueError

        payment_account_id = payment_account_id[0]

        await PaymentRepository(session).pay(ride_id=ride.id, account_id=payment_account_id.id, status_id=status_id,
                                             ammount=bluetooth_devise.transport.price)

        return status_id

        # pay = await PaymentRepository(session).pay(user_id=user_id, ride_id=ride.id)
