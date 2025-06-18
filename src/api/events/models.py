from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, DateTime, SQLModel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


class EventModel(TimescaleModel, table=True):
    """
    Track page visits @ any given time
    page: about/contact/pricing, etc
    """

    page: str = Field(index=True)
    description: Optional[str] = ""
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        # sa_type=TimescaleModel.DateTime(timezone=True), # returns an error
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventListSchema(SQLModel):
    count: int
    results: List[EventModel]


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    count: int


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="my default description")


class EventUpdateSchema(SQLModel):
    """The only field that we allow to be updated via put method"""

    description: str
