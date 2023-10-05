from db.models.preference_accounts import DBPreferenceAccount
from db.models.ride_payments import DBRidePayment
from db.models.sbp_accounts import DBUserSBPAccount
from db.repository.base import BaseRepository

from sqlalchemy import (
    and_,
    select
)


class PaymentRepository(BaseRepository):

    async def pay(self, ride_id: int, account_id: int, status_id: int, ammount: int):
        model = DBRidePayment(
            ride_id=ride_id,
            account_id=account_id,
            status_id=status_id,
            amount=ammount
        )

        await self.add_model(model)

    async def get_payment_account(self, user_id: int) -> list[DBUserSBPAccount]:
        query = (
            select(DBUserSBPAccount)
            .select_from(DBUserSBPAccount)
            .join(DBPreferenceAccount, DBPreferenceAccount.id == DBUserSBPAccount.id, isouter=False)
            .where(
                DBPreferenceAccount.user_id == user_id
            )
            .limit(1)
        )

        return await self.all_ones(query)
