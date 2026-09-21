import asyncio
from app.clients import ms1_client, ms2_client, ms3_client

async def obtener_historial(pasajero_id: int) -> dict:
    pasajero, viajes, conexiones = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id),
        ms3_client.obtener_conexiones_por_pasajero(pasajero_id)
    )

    servicio_ids = list({v["servicio_id"] for v in viajes})
    tarjeta_ids = list({v["tarjeta_id"] for v in viajes})

    paradero_ids = set()
    for v in viajes:
        paradero_ids.add(v["paradero_origen_id"])
        if v.get("paradero_final_id"):
            paradero_ids.add(v["paradero_final_id"])
    for c in conexiones:
        paradero_ids.add(c["paradero_id"])

    servicios, tarjetas, paraderos = await asyncio.gather(
        ms2_client.obtener_servicios_batch(servicio_ids),
        ms1_client.obtener_tarjetas_batch(tarjeta_ids),
        ms2_client.obtener_paraderos_batch(list(paradero_ids))
    )
    servicios_por_id = {s["id"]: s for s in servicios}
    tarjetas_por_id = {t["id"]: t for t in tarjetas}
    paraderos_por_id = {p["id"]: p for p in paraderos}

    ruta_ids = list({s["ruta_id"] for s in servicios})
    rutas = await ms2_client.obtener_rutas_batch(ruta_ids)
    rutas_por_id = {r["id"]: r for r in rutas}

    viajes_enriquecidos = []
    for v in viajes:
        servicio = servicios_por_id.get(v["servicio_id"])
        ruta = rutas_por_id.get(servicio["ruta_id"]) if servicio else None
        tarjeta = tarjetas_por_id.get(v["tarjeta_id"])
        paradero_origen = paraderos_por_id.get(v["paradero_origen_id"])
        paradero_final = paraderos_por_id.get(v.get("paradero_final_id"))

        viajes_enriquecidos.append({
            "id": v["id"],
            "fecha_hora": v["fecha_hora"],
            "ruta_nombre": ruta["nombre"] if ruta else None,
            "tipo_servicio": ruta["tipo_servicio"] if ruta else None,
            "tarjeta_tipo": tarjeta["tipo"] if tarjeta else None,
            "paradero_origen_nombre": paradero_origen["nombre"] if paradero_origen else None,
            "paradero_final_nombre": paradero_final["nombre"] if paradero_final else None,
            "estado": v["estado"]
        })

    conexiones_enriquecidas = []
    for c in conexiones:
        paradero = paraderos_por_id.get(c["paradero_id"])
        conexiones_enriquecidas.append({
            "id": c["id"],
            "viaje_origen_id": c["viaje_origen_id"],
            "viaje_destino_id": c["viaje_destino_id"],
            "paradero_nombre": paradero["nombre"] if paradero else None,
            "fecha_hora": c["fecha_hora"]
        })

    return {
        "pasajero_id": pasajero["id"],
        "nombre": pasajero["nombre"],
        "viajes": viajes_enriquecidos,
        "conexiones": conexiones_enriquecidas
    }