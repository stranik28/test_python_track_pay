from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship


class DBTouche(BaseModel):
    __tablename__ = "touches"

    ride_id = Column(Integer, ForeignKey("ride.id", ondelete="CASCADE"), nullable=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    bluetooth_device_id = Column(Integer, ForeignKey("bluetooth_device.id", ondelete="RESTRICT"), nullable=False)

    ride = relationship("DBRide", lazy="raise", uselist=False)

    user = relationship("DBUser", lazy="raise", uselist=False)

    bluetooth_device = relationship("DBBluetoothDevise", lazy="raise", uselist=False)
