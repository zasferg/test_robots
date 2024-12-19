from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderSchema(Base):
    email: EmailStr
    robot_serial: UUID
