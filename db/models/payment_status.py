from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String
)


class DBPaymentStatus(BaseModel):
    __tablename__ = "payment_status"

    name = Column(String, nullable=False)

    sort = Column(Integer, unique=True)
