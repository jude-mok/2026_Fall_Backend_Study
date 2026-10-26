from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator

from app.database import get_connection

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


app = FastAPI(title="LikeLion Backend Study")


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "project_name": "2026 Fall Backend"}


@app.get("/users", tags=["users"], response_model=UserListResponse)
def list_users(limit: int = Query(default=20, ge=1, le=100)):
    with get_connection() as conn:
        users = conn.execute(
            "SELECT id, name, email FROM public.users ORDER BY id LIMIT %s", (limit,)
        ).fetchall()
    return {"items": users}


@app.get("/users/{user_id}", tags=["users"], response_model=UserResponse)
def read_user(user_id: int):
    with get_connection() as conn:
        user = conn.execute(
            "SELECT id, name, email FROM public.users WHERE id = %s", (user_id,)
        ).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", tags=["users"], status_code=201, response_model=UserResponse)
def create_user(body: UserCreate):
    try:
        with get_connection() as conn:
            user = conn.execute(
                """INSERT INTO public.users (name, email, password_hash)
                   VALUES (%s, %s, %s) RETURNING id, name, email""",
                (body.name, str(body.email), "!dummy-no-login"),
            ).fetchone()
        return user
    except UniqueViolation as exc:
        if exc.diag.constraint_name != "users_email_key":
            raise
        raise HTTPException(status_code=409, detail="Email already exists") from exc


@app.patch("/users/{user_id}", tags=["users"], response_model=UserResponse)
def update_user(user_id: int, body: UserNamePatch):
    with get_connection() as conn:
        user = conn.execute(
            """UPDATE public.users SET name = %s WHERE id = %s
               RETURNING id, name, email""",
            (body.name, user_id),
        ).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", tags=["users"], status_code=204, response_class=Response)
def delete_user(user_id: int):
    with get_connection() as conn:
        deleted = conn.execute(
            "DELETE FROM public.users WHERE id = %s RETURNING id", (user_id,)
        ).fetchone()
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
