import os
from fastapi import APIRouter
from .schemas import (
    EventListSchema,
    EventSchema,
    EventCreateSchema,
    EventUpdateSchema,
)

router = APIRouter()
from api.db.config import DATABASE_URL


# GET /api/events
@router.get("/")
def read_events() -> EventListSchema:
    print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    return {
        "results": [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ],
        "count": 3,
    }


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    return {"id": event_id}


# send data here
# POST /api/events
@router.post("/")
def create_event(payload: EventCreateSchema) -> EventSchema:
    # print(payload.page)
    data = payload.model_dump()  # payload -> dict -> pydantic
    # return {"id": 123, "page": payload.page}
    return {"id": 123, **data}


# UPDATE this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventSchema:
    # print(payload.description)
    # return {"id": event_id, "description": payload.description}
    # data = payload.model_dump(exclude_none=True)
    # print(data)
    data = payload.model_dump()
    return {"id": event_id, **data}


# # DELETE this data
# # DELETE /api/events/12
# @router.delete("/{event_id}")
# def delete_event(event_id: int):
#     return {"id": event_id}
