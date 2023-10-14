from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import relationship


class DBTouche(BaseModel):
    __tablename__ = "touches"

    uuid = Column(String, nullable=False)

    bluetooth_device_id = Column(Integer, ForeignKey("bluetooth_device.id", ondelete="RESTRICT"), nullable=False)

    bluetooth_device = relationship('DBBluetoothDevise', lazy="raise", uselist=False)