import httpx
from app.config import settings

async def obtener_pasajero(pasajero_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.MS1_BASE_URL}/pasajeros/{pasajero_id}")
        response.raise_for_status()
        return response.json()