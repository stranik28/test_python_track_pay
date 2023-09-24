from db.models.bluetooth_device import DBBluetoothDevise
from db.repository.base import BaseRepository
from sqlalchemy import (
    select
)
from sqlalchemy.orm import joinedload

class BluetoothRepository(BaseRepository):

    async def get_by_id(self, bluetooth_id: int) -> DBBluetoothDevise:
        query = (
            select(DBBluetoothDevise)
            .select_from(DBBluetoothDevise)
            .where(
                DBBluetoothDevise.id == bluetooth_id
            )
            .limit(1)
        )

        query = query.options(
            joinedload(DBBluetoothDevise.transport)
        )

        return await self.one_val(query)
