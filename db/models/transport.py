from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    VARCHAR,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import relationship


class DBTransport(BaseModel):
    __tablename__ = "transport"

    type_id = Column(Integer, ForeignKey('transport_type.id', ondelete="RESTRICT"), nullable=False)

    number = Column(VARCHAR(6), nullable=False, unique=True, index=True)

    region_numb = Column(VARCHAR(3), nullable=False)

    price = Column(Integer, nullable=False)

    route_numb = Column(String, nullable=False)

    type = relationship("DBTransportType", lazy="raise", uselist=False)




