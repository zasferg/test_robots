from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CustemerSchema(Base):
    email: EmailStr
