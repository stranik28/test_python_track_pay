import datetime

from db.models.rides import DBRide
from db.repository.base import BaseRepository
from sqlalchemy import (
    select,
    and_,
    desc
)
from db.models.touches import DBTouche
from db.models.bluetooth_device import DBBluetoothDevise
from datetime import datetime, timedelta

from sqlalchemy.orm import joinedload


class RideRepository(BaseRepository):

    async def add_touch(self, bluetooth_id: int, account_id: int) -> None:
        model = DBTouche(
            user_id=account_id,
            bluetooth_device_id=bluetooth_id
        )

        return await self.add_model(model)

    async def get_touch(self, account_id: int) -> list[DBTouche]:
        query = (
            select(DBTouche)
            .select_from(DBTouche)
            .where(
                and_(
                    DBTouche.user_id == account_id,
                    DBTouche.created_at >= datetime.now() - timedelta(minutes=10)
                )
            )
        )

        query = query.options(joinedload(DBTouche.bluetooth_device).joinedload(DBBluetoothDevise.transport))

        return await self.all_ones(query)

    async def create_ride(self, user_id: int, transport_id: int) -> DBRide:
        ride = DBRide(
            user_id=user_id,
            transport_id=transport_id,
            status_id=1
        )

        await self.add_model(ride)

        await self.refresh_model(ride)

        return ride

    @staticmethod
    def _add_ride_options(query):
        query = query.options(
            joinedload(DBRide.status)
        )
        query = query.options(
            joinedload(DBRide.transport)
        )

        return query

    async def get_by_id(self, id_: int) -> list[DBRide]:
        query = (
            select(DBRide)
            .select_from(DBRide)
            .where(DBRide.id == id_)
            .limit(1)
        )

        query = self._add_ride_options(query)

        return await self.all_ones(query)

    async def get_ride(self, user_id: int, transport_id: int) -> list[DBRide]:
        query = (
            select(DBRide)
            .select_from(DBRide)
            .where(
                and_(
                    DBRide.user_id == user_id,
                    DBRide.transport_id == transport_id
                )
            )
            .order_by(desc(DBRide.created_at))
            .limit(1)
        )

        query = self._add_ride_options(query)

        return await self.all_ones(query)
