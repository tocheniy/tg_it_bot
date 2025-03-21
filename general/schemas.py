from datetime import datetime
from pathlib import Path
from pandas import DataFrame
from pydantic import BaseModel, Field, ConfigDict


class EventTgSch(BaseModel):
    type_of: str = Field(serialization_alias="event_type")
    time: datetime = Field(serialization_alias="event_time")
    dvr: str = Field(serialization_alias="dvr_name")
    camera: str | None = Field(default=None, serialization_alias="camera_name")
    city: str | None = Field(default=None, serialization_alias="city")

    # ! - Не нужно
    # chat_id: int | None = Field(default=None)
    # thread: int | None = Field(default=None)


class EventDbSch(BaseModel):
    id: int | None = None
    name: str
    dvr_id: int
    camera: str | None = None
    time: datetime
    model_config = ConfigDict(from_attributes=True)


class EventWithDvrAndDiv(BaseModel):
    name: str | None = None
    ip: str | None = None
    city: str | None = None
    event: EventDbSch
    division_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ChatDbSch(BaseModel):
    id: int | None = None
    name: str
    tg_chat_id: int
    hdd_error: int
    view_tampering: int
    video_signal_lost: int

    model_config = ConfigDict(from_attributes=True)


class EventWithChat(BaseModel):
    chat: ChatDbSch
    event: EventDbSch
    model_config = ConfigDict(from_attributes=True)


class StatSch(BaseModel):
    file_name: str | Path
    event_type: str
    count: int
    data: DataFrame | str
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
