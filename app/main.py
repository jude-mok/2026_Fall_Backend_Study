from fastapi import FastAPI

from app.router.users import router as users_router

app = FastAPI(title="LikeLion Backend Study")
app.include_router(users_router)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "project_name": "2026 Fall Backend"}
