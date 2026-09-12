from fastapi import APIRouter
from app.services import historial_service

router = APIRouter(prefix="/historial", tags=["Historial"])


@router.get("/{pasajero_id}")
async def obtener_historial(pasajero_id: int):
    return await historial_service.obtener_historial(pasajero_id)