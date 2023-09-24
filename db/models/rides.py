from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from db.models.ride_status import DBRideStatus
from db.models.transport import DBTransport
from db.models.transport_type import DBTransportType


class DBRide(BaseModel):
    __tablename__ = "ride"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    transport_id = Column(Integer, ForeignKey("transport.id", ondelete="RESTRICT"), nullable=False)

    status_id = Column(Integer, ForeignKey("ride_status.id", ondelete="RESTRICT"), nullable=False)

    end_at = Column(TIMESTAMP, nullable=True)

    status = relationship("DBRideStatus", lazy="raise", uselist=False)

    transport = relationship("DBTransport", lazy="raise", uselist=False)

    user = relationship("DBUser", lazy="raise", uselist=False)

    @property
    def ride_name(self) -> str:
        return self._ride_name

    @ride_name.setter
    def ride_name(self, ride_name: str):
        self._ride_name = ride_name