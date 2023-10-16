from db.models.bluetooth_device import DBBluetoothDevise
from db.models.user_uuid import DBUuidUsers
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

    async def get_bluetooth_by_esp_id(self, esp_id: int) -> list[DBBluetoothDevise]:

        query = (
            select(DBBluetoothDevise)
            .select_from(DBBluetoothDevise)
            .where(
                DBBluetoothDevise.id == esp_id
            )
            .limit(1)
        )

        query = query.options(
            joinedload(DBBluetoothDevise.transport))

        return await self.all_ones(query)

    async def set_new_notification_info(self, user_id, devise_token, devise_uuid):

        model = DBUuidUsers(
            user_id=user_id,
            uuid=devise_uuid,
            token=devise_token
        )

        await self.add_model(model)

    async def get_notification_by_id(self, user_id):
        query = (
            select(DBUuidUsers)
            .select_from(DBUuidUsers)
            .where(
                DBUuidUsers.user_id == user_id
            )
        )

        return await self.all_ones(query)
