from pydantic import BaseModel, Field
from typing import List, Optional


class EventSchema(BaseModel):
    id: int
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventListSchema(BaseModel):
    count: int
    results: List[EventSchema]


class EventCreateSchema(BaseModel):
    page: str
    description: Optional[str] = Field(default="my default description")


class EventUpdateSchema(BaseModel):
    """The only field that we allow to be updated via put method"""

    description: str
