import datetime
from typing import Optional

import sqlalchemy.types as types
from sqlalchemy import Column, text, MetaData
from sqlalchemy.orm import declarative_base

meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}, schema=None)

Base = declarative_base(metadata=meta)   # type: ignore


class BaseModel(Base):
    __abstract__ = True

    id = Column(types.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(
        types.TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        types.TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP')
    )

    __mapper_args__ = {"eager_defaults": True}

    @property
    def created_at_timestamp(self) -> int:
        return int(self.created_at.timestamp())

    @property
    def updated_at_timestamp(self) -> int:
        return int(self.updated_at.timestamp())

    def set_updated_at(self, date_time: Optional[datetime.datetime] = None) -> None:
        if date_time:
            self.updated_at = date_time
        else:
            self.updated_at = datetime.datetime.now()