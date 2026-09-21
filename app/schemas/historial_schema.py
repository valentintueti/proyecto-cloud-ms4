from pydantic import BaseModel
from typing import List, Optional

class ViajeEnriquecido(BaseModel):
    id: int
    fecha_hora: str
    ruta_nombre: Optional[str] = None
    tipo_servicio: Optional[str] = None
    tarjeta_tipo: Optional[str] = None
    paradero_origen_nombre: Optional[str] = None
    paradero_final_nombre: Optional[str] = None
    estado: str

class ConexionEnriquecida(BaseModel):
    id: int
    viaje_origen_id: int
    viaje_destino_id: int
    paradero_nombre: Optional[str] = None
    fecha_hora: str

class HistorialResponse(BaseModel):
    pasajero_id: int
    nombre: str
    viajes: List[ViajeEnriquecido]
    conexiones: List[ConexionEnriquecida]