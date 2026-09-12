from fastapi import FastAPI
from app.routers import historial_router

app = FastAPI(title="MS4 - Historial")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(historial_router.router)