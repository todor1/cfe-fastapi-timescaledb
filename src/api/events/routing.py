from sqlalchemy import func, case
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Query
from api.db.session import get_session
from .models import (
    EventModel,
    EventBucketSchema,
    EventCreateSchema,
)
from timescaledb.hyperfunctions import time_bucket
from typing import List

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
    "/",
    "/about",
    "/pricing",
    "/contact",
    "/blog",
    "/products",
    "/login",
    "/signup",
    "/dashboard",
    "/settings",
]


# GET /api/events
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session),
):
    os_case = case(
        (EventModel.user_agent.ilike("%windows%"), "Windows"),
        (EventModel.user_agent.ilike("%macintosh%"), "MacOS"),
        (EventModel.user_agent.ilike("%iphone%"), "iOS"),
        (EventModel.user_agent.ilike("%android%"), "Android"),
        (EventModel.user_agent.ilike("%linux%"), "Linux"),
        else_="Other",
    ).label("operating_system")
    # bucket width and time field in the db table
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = (
        pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    )
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.round(func.avg(EventModel.duration), 2).label("avg_duration"),
            func.count().label("count"),
        )
        .where(EventModel.page.in_(lookup_pages))
        .group_by(bucket, os_case, EventModel.page)
        .order_by(bucket, os_case, EventModel.page)
    )
    results = session.exec(query).all()
    return results


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found.")
    return result


# SEND data here
# POST /api/events
@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()  # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)  # preparing to add to the db
    session.commit()  # actually writing to the db
    session.refresh(obj)
    return obj


# # DELETE this data
# # DELETE /api/events/123
@router.delete("/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)):
    obj = session.get(EventModel, event_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found.")
    session.delete(obj)
    session.commit()
    return {"ok": True}
