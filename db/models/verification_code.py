from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship


class DBVerifyCode(BaseModel):
    __tablename__ = "verify_code"

    account_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    code = Column(Integer, nullable=False)

    used = Column(Boolean, nullable=False, server_default="false")

    type_of_code = Column(Integer, nullable=False)
    # 0 - Verify
    # 1 - Recover

    account = relationship("DBUser", uselist=False)
