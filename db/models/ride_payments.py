from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)


class DBRidePayment(BaseModel):
    __tablename__ = "ride_payment"

    ride_id = Column(Integer, ForeignKey("ride.id", ondelete="RESTRICT"), nullable=False)

    account_id = Column(Integer, ForeignKey("sbp_account.id", ondelete="CASCADE"), nullable=False)

    amount = Column(Integer, nullable=False)

    status_id = Column(Integer, ForeignKey("payment_status.id"), nullable=False)