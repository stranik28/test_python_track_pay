from sqlalchemy import (
    select
)

from db.models.users import DBUser
from db.repository.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_user_by_id(self, user_id: int) -> list[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(DBUser.id == user_id)
            .limit(1)
        )

        return await self.all_ones(query)
