import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bluetooth_device import DBBluetoothDevise
from db.models.rides import DBRide
from db.models.user_uuid import DBUuidUsers
from db.models.users import DBUser
from db.repository.bluetooth import BluetoothRepository
from db.repository.ride import RideRepository

from db.models.touches import DBTouche
from db.repository.user import UserRepository

from vendors.const import months
from vendors.exception import BluetoothNotFound, RideNotFound, AccessDenied, UserNotFound, NotSureToCreateRide, \
    EspNotFound, RideAlreadyDone


class RideManager:

    @staticmethod
    def _set_ride_name(ride: DBRide) -> DBRide:
        date = ride.created_at.day
        month = ride.created_at.month
        hours = ride.created_at.hour
        minutes = ride.created_at.minute
        name = f"Поездка {date} {months[month - 1]} в {hours}:{minutes}"

        print(name)

        ride.ride_name = name

        return ride

    @classmethod
    async def touch(cls, session: AsyncSession, bluetooth_mac: str, user_id: int) -> DBRide:
        bluetooth: list[DBBluetoothDevise] = await BluetoothRepository(session).get_by_id(bluetooth_mac=bluetooth_mac)

        if not bluetooth:
            raise BluetoothNotFound

        bluetooth = bluetooth[0]

        ride: DBRide = await RideRepository(session).create_ride(transport_id=bluetooth.transport.id,
                                                                 user_id=user_id)
        ride: list[DBRide] = await RideRepository(session).get_by_id(id_=ride.id)

        ride = ride[0]

        ride = cls._set_ride_name(ride)

        return ride

    @staticmethod
    async def change_status(session: AsyncSession, status_id: int, ride_id: int) -> None:
        ride: list[DBRide] = await RideRepository(session).get_by_id(id_=ride_id)

        ride = ride[0]

        ride.status_id = status_id

        await session.commit()



    @staticmethod
    async def ride_history(session: AsyncSession, user_id: int, limit: int, offset: int) -> list[DBRide]:
        return await RideRepository(session).get_ride_history(user_id=user_id,
                                                              limit=limit,
                                                              offset=offset)

    @classmethod
    async def get_ride(cls, session: AsyncSession, ride_id: int, user_id: int) -> DBRide:
        ride: list[DBRide] = await RideRepository(session).get_by_id(id_=ride_id)

        if ride == [] or ride is None:
            raise RideNotFound
        ride = ride[0]
        if ride.user_id != user_id:
            raise AccessDenied

        ride = cls._set_ride_name(ride)

        return ride

    @staticmethod
    async def send_message(registration_token: str, ride_id: int):
        from firebase_admin import messaging
        message = messaging.Message(
            notification=messaging.Notification(
                title="Оплати проезд!",
                body="Вы в автобусе!"
            ),
            android=messaging.AndroidConfig(
                priority="high"  # Высокий приоритет
            ),
            token=registration_token,
            data={
                "id": str(ride_id)
            }
        )
        response = messaging.send(message)
        print(response)

    @classmethod
    async def esp_touch(cls, session: AsyncSession, uuid: str, esp_id: int, admin: Optional[bool] = None):
        user_exist: list[DBUuidUsers] = await UserRepository(session).get_user_by_uuid(uuid)
        if user_exist == []:
            print("User")
            raise UserNotFound
        user_exist = user_exist[0]
        user_exist_users_tokens = user_exist
        user_exist = user_exist[0]

        await RideRepository(session).add_touch(uuid=uuid, esp_id=esp_id)
        # timdelta = datetime.timedelta(minutes=10)
        timdelta = datetime.timedelta(seconds=40)
        last_touches: list[int] = await RideRepository(session).count_last_touche(uuid=uuid, time=timdelta)

        if last_touches != []:
            if last_touches[0] < 1:
                print("Not sure")
                raise NotSureToCreateRide

        esp: list[DBBluetoothDevise] = await BluetoothRepository(session).get_bluetooth_by_esp_id(esp_id=esp_id)

        if esp == []:
            print("esp")
            raise EspNotFound

        esp = esp[0]
        timedelta_ = datetime.timedelta(minutes=1)
        last_ride = await RideRepository(session).get_full_ride_history(user_id=user_exist.id, timedelta_=timedelta_,
                                                                        transport_id=esp.transport.id, limit=1, offset=0)

        if last_ride != [] and not admin:
            print("Уже покатался")
            raise RideAlreadyDone

        ride = await RideRepository(session).create_ride(user_id=user_exist.id, transport_id=esp.transport.id)

        # Send push

        print("Success Ride")
        print(user_exist.token)
        print(ride.id)
        await cls.send_message(registration_token=user_exist.token, ride_id=ride.id)

        return ride
