from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bluetooth_device import DBBluetoothDevise
from db.models.rides import DBRide
from db.repository.bluetooth import BluetoothRepository
from db.repository.ride import RideRepository

from db.models.touches import DBTouche

from vendors.const import months
from vendors.exception import BluetoothNotFound, RideNotFound, AccessDenied


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

    @staticmethod
    async def ride_history(session: AsyncSession, user_id: int, limit: int, offset: int) -> list[DBRide]:
        return await RideRepository(session).get_ride_history(user_id=user_id,
                                                              limit=limit,
                                                              offset=offset)

    @staticmethod
    async def get_ride(session: AsyncSession, ride_id: int, user_id: int) -> DBRide:
        ride: list[DBRide] = await RideRepository(session).get_by_id(id_=ride_id)

        if ride == [] or ride is None:
            raise RideNotFound
        ride = ride[0]
        if ride.user_id != user_id:
            raise AccessDenied

        return ride

