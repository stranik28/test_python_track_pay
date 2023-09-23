from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship


class DBBluetoothDevise(BaseModel):
    __tablename__ = "bluetooth_device"

    transport_id = Column(Integer, ForeignKey("transport.id", ondelete="CASCADE"), nullable=False)

    transport = relationship("DBTransport", lazy="raise", uselist=False)