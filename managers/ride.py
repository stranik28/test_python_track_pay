from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bluetooth_device import DBBluetoothDevise
from db.models.rides import DBRide
from db.repository.bluetooth import BluetoothRepository
from db.repository.ride import RideRepository

from db.models.touches import DBTouche

from vendors.const import months


class RideManager:

    @staticmethod
    def _set_ride_name(ride: DBRide) -> DBRide:
        date = ride.created_at.day
        month = ride.created_at.month
        hours = ride.created_at.hour
        minutes = ride.created_at.minute
        name = f"Поездка {date} {months[month-1]} в {hours}:{minutes}"

        print(name)

        # print(ride.created_at.strftime("%d %B"))
        ride.ride_name = name

        return ride

    @classmethod
    async def touch(cls, session: AsyncSession, bluetooth_id: int, user_id: int) -> DBRide:

        await RideRepository(session).add_touch(bluetooth_id=bluetooth_id, account_id=user_id)

        bluetooth: list[DBBluetoothDevise] = await BluetoothRepository(session).get_by_id(bluetooth_id=bluetooth_id)

        if not bluetooth:
            return 0

        bluetooth = bluetooth

        touches: list[DBTouche] = await RideRepository(session).get_touch(account_id=user_id)

        same_touch = 0

        for i in touches:
            if i.bluetooth_device.transport.id == bluetooth.transport.id:
                same_touch += 1

        if same_touch != 0:
            ride: DBRide = await RideRepository(session).get_ride(user_id=user_id, transport_id=bluetooth.transport.id)
        else:
            ride: DBRide = await RideRepository(session).create_ride(transport_id=bluetooth.transport.id,
                                                                     user_id=user_id)
        ride = ride[0]
        ride = cls._set_ride_name(ride)

        return ride
        # background task
        # if same_touch == 0:
        #     return False
        # if same_touch > 5 and ((len(touches) / same_touch) > 0.75):
        #     ride: DBRide = await RideRepository(session).create_ride(transport_id=transport_id, user_id=user_id)
        #
        #     return True
        # else:
        #     return False
