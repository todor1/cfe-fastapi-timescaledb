from datetime import datetime, timezone
from typing import List, Optional

# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field
from timescaledb import TimescaleModel

def get_utc_now():
    """
    Why use .replace(tzinfo=timezone.utc) after already using datetime.now(timezone.utc)?
    In most cases, this is unnecessary because datetime.now(timezone.utc) already returns a timezone-aware object.
    However, there are a few edge cases where someone might do this:
    - To ensure consistency if the code is reused or modified later.
    - To normalize the timezone info in case it came from a different source or was altered.
    - To forcefully overwrite any existing tzinfo (though in this case, it's already UTC).

    dt = datetime.now(timezone.utc)
    print(dt)  # e.g., 2025-06-15 11:54:08.123456+00:00

    dt_fixed = dt.replace(tzinfo=timezone.utc)
    print(dt_fixed)  # Same output, but tzinfo is explicitly set again

    The code is functionally equivalent to just datetime.now(timezone.utc),
    and the .replace() part is usually redundant unless you're trying to enforce or reset the timezone info explicitly.
    """
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )


class EventListSchema(SQLModel):
    count: int
    results: List[EventModel]


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="my default description")


class EventUpdateSchema(SQLModel):
    """The only field that we allow to be updated via put method"""

    description: str
