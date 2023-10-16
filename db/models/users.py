from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Boolean,
    text,
    Text,
    VARCHAR,
    Integer,
    String
)


class DBUser(BaseModel):
    __tablename__ = "user"

    username = Column(String, nullable=False)

    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    middle_name = Column(Text, nullable=True)

    phone_number = Column(Text, nullable=True, unique=True)
    email = Column(VARCHAR(63), nullable=True, unique=True)
    active = Column(Boolean, server_default=text("false"))

    password = Column(Text, nullable=True)

    block = Column(Boolean, nullable=False, server_default=text("false"))

    limit_rides = Column(Integer, nullable=True)
