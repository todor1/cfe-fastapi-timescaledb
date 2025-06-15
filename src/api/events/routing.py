from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api.db.session import get_session
from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now,
)


router = APIRouter()


# GET /api/events
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    # query = select(EventModel).order_by(EventModel.id.asc()).limit(10)
    query = select(EventModel).order_by(EventModel.updated_at.desc()).limit(10)
    results = session.exec(query).all()
    return {"results": results, "count": len(results)}


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found.")
    return result


# UPDATE this data
# PUT /api/events/12
@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id: int,
    payload: EventUpdateSchema,
    session: Session = Depends(get_session),
):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found.")
    data = payload.model_dump()
    # change respective fields in object with payload values
    for k, v in data.items():
        if k == "id":
            continue
        setattr(obj, k, v)
    obj.updated_at = get_utc_now()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


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
