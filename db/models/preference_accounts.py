from db.models.base import BaseModel

from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)


class DBPreferenceAccount(BaseModel):
    __tablename__ = "preference_account"

    account_id = Column(Integer, ForeignKey('sbp_account.id', ondelete="CASCADE"), nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("DBUser", lazy="raise", uselist=False)

    account = relationship("DBUserSBPAccounts", lazy='raise', uselist=False)
