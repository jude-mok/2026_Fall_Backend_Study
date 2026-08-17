from fastapi import FastAPI

app = FastAPI(title="LikeLion Backend Study")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "project_name": "2026 Fall Backend"}
