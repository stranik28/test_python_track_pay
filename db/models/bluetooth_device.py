from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import relationship


class DBBluetoothDevise(BaseModel):
    __tablename__ = "bluetooth_device"

    transport_id = Column(Integer, ForeignKey("transport.id", ondelete="CASCADE"), nullable=False)

    mac_address = Column(String, unique=True, nullable=False, index=True)

    transport = relationship("DBTransport", lazy="raise", uselist=False)