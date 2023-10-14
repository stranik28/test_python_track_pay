from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import relationship


class DBUuidUsers(BaseModel):
    __tablename__ = "uuid_device"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    uuid = Column(String, nullable=False, index=True)

    token = Column(String, nullable=False, index=True)

    user = relationship("DBUser", lazy="raise", uselist=False)
