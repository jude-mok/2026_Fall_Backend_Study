from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator

UserName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: UserName
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class UserNamePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: UserName


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class UserListResponse(BaseModel):
    items: list[UserResponse]
