from fastapi import APIRouter, HTTPException, Query, Response
from psycopg.errors import UniqueViolation

from app.model.users import UserCreate, UserListResponse, UserNamePatch, UserResponse
from app.repository import users as user_repository
router = APIRouter()


@router.get("/users", tags=["users"], response_model=UserListResponse)
def list_users(limit: int = Query(default=20, ge=1, le=100)):
    return {"items": user_repository.get_all_users(limit)}


@router.get("/users/{user_id}", tags=["users"], response_model=UserResponse)
def read_user(user_id: int):
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", tags=["users"], status_code=201, response_model=UserResponse)
def create_user(body: UserCreate):
    try:
        return user_repository.create_user(body.name, str(body.email))
    except UniqueViolation as exc:
        if exc.diag.constraint_name != "users_email_key":
            raise
        raise HTTPException(status_code=409, detail="Email already exists") from exc


@router.patch("/users/{user_id}", tags=["users"], response_model=UserResponse)
def update_user(user_id: int, body: UserNamePatch):
    user = user_repository.update_user_name(user_id, body.name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", tags=["users"], status_code=204, response_class=Response)
def delete_user(user_id: int):
    deleted = user_repository.delete_user(user_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)