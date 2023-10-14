from db.models.rides import DBRide
from db.models.transport import DBTransport
from db.repository.base import BaseRepository
from sqlalchemy import (
    select,
    and_,
    desc,
    func
)
from db.models.touches import DBTouche
from db.models.bluetooth_device import DBBluetoothDevise
from datetime import datetime, timedelta

from sqlalchemy.orm import joinedload, selectinload


class RideRepository(BaseRepository):

    async def add_touch(self, esp_id: int, uuid: str) -> None:
        model = DBTouche(
            bluetooth_device_id=esp_id,
            uuid=uuid
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

    async def create_ride(self, user_id: int, transport_id: int, status_id: int = 1) -> DBRide:
        ride = DBRide(
            user_id=user_id,
            transport_id=transport_id,
            status_id=status_id
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
            selectinload(DBRide.transport).joinedload(DBTransport.type)
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

    async def get_ride_history(self, user_id: int, limit: int, offset: int) -> list[DBRide]:
        query = (
            select(DBRide)
            .select_from(DBRide)
            .where(
                and_(
                    DBRide.user_id == user_id,
                    DBRide.status_id == 2
                )
            )
            .order_by(desc(DBRide.created_at))
            .limit(limit)
            .offset(offset)
        )

        query = self._add_ride_options(query)

        return await self.all_ones(query)

    async def count_last_touche(self, uuid: str, time: timedelta):
        end_time = datetime.now()
        start_time = end_time - time
        query = (
            select(func.count(DBTouche.id))
            .select_from(DBTouche)
            .where(
                and_(
                    DBTouche.uuid == uuid,
                    DBTouche.created_at >= start_time,
                )
            )
        )

        return await self.all_ones(query)

    # 0000fef3-0000-1000-8000-00805f9b34fb

    async def get_full_ride_history(self, user_id: int, limit: int, offset: int) -> list[DBRide]:
        query = (
            select(DBRide)
            .select_from(DBRide)
            .where(
                and_(
                    DBRide.user_id == user_id,
                )
            )
            .order_by(desc(DBRide.created_at))
            .limit(limit)
            .offset(offset)
        )

        return await self.all_ones(query)