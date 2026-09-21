import httpx
from app.config import settings
from app.core.exceptions import NotFoundError, ExternalServiceError

async def obtener_pasajero(pasajero_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.MS1_BASE_URL}/pasajeros/{pasajero_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise NotFoundError(f"Pasajero {pasajero_id} no encontrado en MS1")
            raise ExternalServiceError(f"Error al consultar MS1: {e}")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS1: {e}")

async def obtener_tarjetas_batch(ids: list[int]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS1_BASE_URL}/tarjetas/batch",
                params={"ids": ",".join(str(i) for i in ids)}
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS1: {e}")