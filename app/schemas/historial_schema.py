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

class ViajesResponse(BaseModel):
    pasajero_id: int
    viajes: List[ViajeEnriquecido]

class ResumenResponse(BaseModel):
    pasajero_id: int
    total_viajes: int
    total_conexiones: int
    tipo_servicio_mas_usado: Optional[str] = None
    ultimo_viaje: Optional[str] = None

class TarjetaConUso(BaseModel):
    id: int
    tipo: str
    saldo: float
    veces_usada: int

class TarjetasResponse(BaseModel):
    pasajero_id: int
    tarjetas: List[TarjetaConUso]