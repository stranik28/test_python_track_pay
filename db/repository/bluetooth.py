from db.models.bluetooth_device import DBBluetoothDevise
from db.repository.base import BaseRepository
from sqlalchemy import (
    select
)
from sqlalchemy.orm import joinedload


class BluetoothRepository(BaseRepository):

    async def get_by_id(self, bluetooth_mac: str) -> DBBluetoothDevise:
        query = (
            select(DBBluetoothDevise)
            .select_from(DBBluetoothDevise)
            .where(
                DBBluetoothDevise.mac_address == bluetooth_mac
            )
            .limit(1)
        )

        query = query.options(
            joinedload(DBBluetoothDevise.transport)
        )

        return await self.all_ones(query)
