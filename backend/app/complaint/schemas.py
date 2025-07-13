from datetime import datetime
from pydantic import BaseModel, constr

class ComplaintCreate(BaseModel):
    text: constr(min_length=1, strip_whitespace=True)

class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str | None = None

    class Config:
        from_attributes = True


class ComplaintBackendResponse(BaseModel):
    id: int
    status: str
    text: str
    sentiment: str
    category: str | None = None
    timestamp: datetime | None = None
    ip_country: str | None = None

    class Config:
        from_attributes = True