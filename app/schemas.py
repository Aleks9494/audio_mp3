from pydantic import (
    BaseModel,
    UUID4,
    HttpUrl,
    Field
)


class UserCreate(BaseModel):
    username: str


class UserResponse(BaseModel):
    success: bool = True
    id: int
    token: UUID4 = Field(...)


class SongResponse(BaseModel):
    success: bool = True
    url: HttpUrl


class SongDB(BaseModel):
    id: int
    uuid_key: UUID4
    name: str
    song: bytes
    user_id: int

    class Config:
        orm_mode = True