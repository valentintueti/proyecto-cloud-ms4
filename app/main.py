from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import historial_router
from app.core.exceptions import NotFoundError, ExternalServiceError

app = FastAPI(title="MS4 - Historial")


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


@app.exception_handler(ExternalServiceError)
async def external_service_handler(request: Request, exc: ExternalServiceError):
    return JSONResponse(status_code=502, content={"detail": exc.detail})


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(historial_router.router)