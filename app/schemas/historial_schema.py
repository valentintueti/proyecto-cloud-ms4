from pydantic import BaseModel
from typing import List, Optional


class ViajeEnriquecido(BaseModel):
    id: int
    fecha_hora: str
    ruta_nombre: Optional[str] = None
    tipo_servicio: Optional[str] = None
    estado: str


class HistorialResponse(BaseModel):
    pasajero_id: int
    nombre: str
    viajes: List[ViajeEnriquecido]