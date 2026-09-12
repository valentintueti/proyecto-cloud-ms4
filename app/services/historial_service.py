import asyncio
from app.clients import ms1_client, ms2_client, ms3_client


async def obtener_historial(pasajero_id: int) -> dict:
    pasajero, viajes = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id)
    )

    servicio_ids = list({v["servicio_id"] for v in viajes})
    servicios = await ms2_client.obtener_servicios_batch(servicio_ids)
    servicios_por_id = {s["id"]: s for s in servicios}

    ruta_ids = list({s["ruta_id"] for s in servicios})
    rutas = await ms2_client.obtener_rutas_batch(ruta_ids)
    rutas_por_id = {r["id"]: r for r in rutas}

    viajes_enriquecidos = []
    for v in viajes:
        servicio = servicios_por_id.get(v["servicio_id"])
        ruta = rutas_por_id.get(servicio["ruta_id"]) if servicio else None

        viajes_enriquecidos.append({
            "id": v["id"],
            "fecha_hora": v["fecha_hora"],
            "ruta_nombre": ruta["nombre"] if ruta else None,
            "tipo_servicio": ruta["tipo_servicio"] if ruta else None,
            "estado": v["estado"]
        })

    return {
        "pasajero_id": pasajero["id"],
        "nombre": pasajero["nombre"],
        "viajes": viajes_enriquecidos
    }