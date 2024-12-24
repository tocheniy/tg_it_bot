from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class EventTgSch(BaseModel):
    type_of: str = Field(serialization_alias="event_type")
    time: datetime = Field(serialization_alias="event_time")
    dvr: str = Field(serialization_alias="dvr_name")
    camera: str | None = Field(default=None, serialization_alias="camera_name")
    city: str | None = Field(default=None, serialization_alias="city")
    chat_id: int | None = Field(default=None)
    thread: int | None = Field(default=None)


class EventDbSch(BaseModel):
    id: int | None = None
    name: str
    dvr_id: int
    camera: str | None = None
    time: datetime
    model_config = ConfigDict(from_attributes=True)


class EventWithDvr(BaseModel):
    name: str | None = None
    ip: str | None = None
    city: str | None = None
    event: EventDbSch
    model_config = ConfigDict(from_attributes=True)
