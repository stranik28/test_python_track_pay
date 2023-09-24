from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import DBUser

from db.repository.user import UserRepository


class UserManager:

    @staticmethod
    async def get_user(user_id: int, session: AsyncSession) -> DBUser:
        user: list[DBUser] = await UserRepository(session).get_user_by_id(user_id=user_id)

        if user_id is None or user == []:
            return None

        return user[0]
