from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RobotSchema(Base):
    serial: UUID
    model: str
    version: str
    created: datetime
