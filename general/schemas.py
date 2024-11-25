from pydantic import BaseModel, Field


class EventTo(BaseModel):
    type_of: str = Field(serialization_alias="event_type")
    time: str = Field(serialization_alias="event_time")
    dvr: str = Field(serialization_alias="dvr_name")
    camera: str | None = Field(default=None, serialization_alias="camera_name")
    city: str | None = Field(default=None, serialization_alias="city")
    chat_id: int | None = Field(default=None)
    thread: int | None = Field(default=None)
