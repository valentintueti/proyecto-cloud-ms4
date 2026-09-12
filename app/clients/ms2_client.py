import httpx
from app.config import settings

async def obtener_servicios_batch(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.MS2_BASE_URL}/servicios/batch",
            params={"ids": ",".join(ids)}
        )
        response.raise_for_status()
        return response.json()

async def obtener_rutas_batch(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.MS2_BASE_URL}/rutas/batch",
            params={"ids": ",".join(ids)}
        )
        response.raise_for_status()
        return response.json()