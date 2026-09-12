import httpx
from app.config import settings

async def obtener_viajes_por_pasajero(pasajero_id: int) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.MS3_BASE_URL}/viajes",
            params={"pasajero_id": pasajero_id}
        )
        response.raise_for_status()
        return response.json()