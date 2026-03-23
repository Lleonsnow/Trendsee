from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class UserUpdateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str


class UserTokenResponse(BaseModel):
    token: str
    user: UserResponse

