from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    text
)

from sqlalchemy.orm import relationship


class DBUserSBPAccount(BaseModel):
    __tablename__ = "sbp_account"

    account_id = Column(Integer, nullable=False, index=True)

    active = Column(Boolean, nullable=False, server_default=text("true"))

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("DBUser", uselist=False, lazy="raise")
