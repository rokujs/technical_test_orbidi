from fastapi import FastAPI

from app.routers import location_api, category_api, suggestion_api

app = FastAPI()

app.include_router(location_api.router)
app.include_router(category_api.router)
app.include_router(suggestion_api.router)

@app.get("/health")
async def health():
    return {"status": "ok"}