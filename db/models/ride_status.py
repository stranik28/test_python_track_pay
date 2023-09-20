from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String
)


class DBRideStatus(BaseModel):
    __tablename__ = "ride_status"

    name = Column(String, nullable=False)

    sort = Column(Integer, unique=True)
