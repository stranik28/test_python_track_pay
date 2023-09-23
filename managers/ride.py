from sqlalchemy.ext.asyncio import AsyncSession

from db.models.rides import DBRide
from db.repository.ride import RideRepository

from db.models.touches import DBTouche


class RideManager:

    @classmethod
    async def touch(cls, session: AsyncSession, bluetooth_id: int, user_id: int):

        await RideRepository(session).add_touch(bluetooth_id=bluetooth_id, account_id=user_id)

        touches: list[DBTouche] = await RideRepository(session).get_touch(account_id=user_id)

        transport_id = 0

        same_touch = 0
        for i in touches:
            if i.bluetooth_device_id == bluetooth_id:
                transport_id = i.bluetooth_device.transport.id
                same_touch += 1

        # background task
        print(same_touch)
        if same_touch == 0:
            return False
        print(len(touches) / same_touch > 0.75)
        if same_touch > 5 and ((len(touches) / same_touch) > 0.75):
            ride: DBRide = await RideRepository(session).create_ride(transport_id=transport_id, user_id=user_id)

            # if await RideRepository(session).pay():
            #
            return True
        else:
            return False
