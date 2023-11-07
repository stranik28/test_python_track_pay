from datetime import datetime, timedelta
from typing import Optional

from db.models.preference_accounts import DBPreferenceAccount
from db.models.ride_payments import DBRidePayment
from db.models.sbp_accounts import DBUserSBPAccount
from db.repository.base import BaseRepository

from sqlalchemy import (
    and_,
    select
)


class PaymentRepository(BaseRepository):

    async def pay(self, ride_id: int, account_id: Optional[int], status_id: int, ammount: int):

        # Добавьте интервал к текущему времени

        model = DBRidePayment(
            ride_id=ride_id,
            # account_id=account_id,
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

    async def add_payment(self,
                          user_id: int,
                          sbp_account: int) -> DBUserSBPAccount:

        model = DBUserSBPAccount(
            account_id=user_id,
            user_id=sbp_account
        )

        await self.add_model(model)

        return await self.refresh_model(model)

    async def get_by_sbp_account(self, user_id: int, payment_id: int) -> list[DBUserSBPAccount]:

        query = (
            select(DBUserSBPAccount)
            .select_from(DBUserSBPAccount)
            .where(
                and_(
                    DBUserSBPAccount.user_id == user_id,
                    DBUserSBPAccount.id == payment_id
                )
            )
        )

        return await self.all_ones(query)

    async def create_new_payment_main(self, user_id: int, payment_account: int) -> None:

        model = DBPreferenceAccount(
            user_id=user_id,
            account_id=payment_account
        )

        await self.add_model(model)

    async def get_payments_account(self, user_id: int) -> list[DBUserSBPAccount]:

        query = (
            select(DBUserSBPAccount)
            .select_from(DBUserSBPAccount)
            .where(
                DBUserSBPAccount.user_id == user_id
            )
        )

        return await self.all_ones(query)