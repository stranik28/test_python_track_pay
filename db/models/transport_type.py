from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    String
)


class DBTransportType(BaseModel):
    __tablename__ = "transport_type"

    name = Column(String, nullable=False)
