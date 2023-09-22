from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Boolean,
    text,
    Text,
    VARCHAR,
    Integer
)


class DBUser(BaseModel):
    __tablename__ = "user"

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    middle_name = Column(Text, nullable=False)

    phone_number = Column(Text, nullable=True, unique=True)
    email = Column(VARCHAR(63), nullable=True, unique=True)
    active = Column(Boolean, server_default=text("false"))

    password = Column(Text, nullable=False)

    block = Column(Boolean, nullable=False, server_default=text("false"))

    limit_rides = Column(Integer, nullable=True)


