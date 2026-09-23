import httpx
from app.config import settings
from app.core.exceptions import ExternalServiceError


async def obtener_viajes_por_pasajero(pasajero_id: int) -> list[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS3_BASE_URL}/viajes",
                params={"pasajero_id": pasajero_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"MS3 respondió con error ({e.response.status_code}) al pedir viajes")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS3: {e}")


async def obtener_conexiones_por_pasajero(pasajero_id: int) -> list[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS3_BASE_URL}/conexiones/pasajero/{pasajero_id}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"MS3 respondió con error ({e.response.status_code}) al pedir conexiones")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS3: {e}")