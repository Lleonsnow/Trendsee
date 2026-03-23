from pydantic import BaseModel, Field, model_validator


class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1)


class PostUpdateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    text: str | None = Field(default=None)

    @model_validator(mode='after')
    def validate_at_least_one(self) -> 'PostUpdateRequest':
        if self.title is None and self.text is None:
            raise ValueError('Не задано ни одного поля для обновления')
        return self


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    created_at: str
    updated_at: str


class PostsFeedResponse(BaseModel):
    items: list[PostResponse]
    total: int
    has_more: bool

