from fastapi import APIRouter
from app.services import historial_service
from app.schemas.historial_schema import (
    HistorialResponse, ViajesResponse, ResumenResponse, TarjetasResponse
)

router = APIRouter(prefix="/historial", tags=["Historial"])

@router.get("/{pasajero_id}", response_model=HistorialResponse)
async def obtener_historial(pasajero_id: int):
    return await historial_service.obtener_historial(pasajero_id)

@router.get("/{pasajero_id}/viajes", response_model=ViajesResponse)
async def obtener_viajes(pasajero_id: int):
    return await historial_service.obtener_viajes(pasajero_id)

@router.get("/{pasajero_id}/resumen", response_model=ResumenResponse)
async def obtener_resumen(pasajero_id: int):
    return await historial_service.obtener_resumen(pasajero_id)

@router.get("/{pasajero_id}/tarjetas", response_model=TarjetasResponse)
async def obtener_tarjetas(pasajero_id: int):
    return await historial_service.obtener_tarjetas(pasajero_id)