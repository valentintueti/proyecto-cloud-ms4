from fastapi import APIRouter
from app.services import historial_service
from app.schemas.historial_schema import HistorialResponse

router = APIRouter(prefix="/historial", tags=["Historial"])

@router.get("/{pasajero_id}", response_model=HistorialResponse)
async def obtener_historial(pasajero_id: int):
    return await historial_service.obtener_historial(pasajero_id)