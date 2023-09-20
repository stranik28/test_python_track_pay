from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)


class DBBluetoothDevise(BaseModel):
    __tablename__ = "bluetooth_device"

    transport_id = Column(Integer, ForeignKey("transport.id", ondelete="CASCADE"), nullable=False)