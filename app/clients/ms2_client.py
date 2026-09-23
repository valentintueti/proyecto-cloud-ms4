import httpx
from app.config import settings
from app.core.exceptions import NotFoundError, ExternalServiceError


async def obtener_servicios_batch(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS2_BASE_URL}/servicios/batch",
                params={"ids": ",".join(ids)}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"MS2 respondió con error ({e.response.status_code}) al pedir servicios")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS2: {e}")


async def obtener_rutas_batch(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS2_BASE_URL}/rutas/batch",
                params={"ids": ",".join(ids)}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"MS2 respondió con error ({e.response.status_code}) al pedir rutas")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS2: {e}")


async def obtener_paraderos_batch(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.MS2_BASE_URL}/paraderos/batch",
                params={"ids": ",".join(ids)}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"MS2 respondió con error ({e.response.status_code}) al pedir paraderos")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"No se pudo conectar a MS2: {e}")