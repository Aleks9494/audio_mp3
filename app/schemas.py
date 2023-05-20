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
