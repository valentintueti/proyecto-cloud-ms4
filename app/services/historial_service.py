import asyncio
from app.clients import ms1_client, ms2_client, ms3_client

async def _resolver_relacionados(viajes: list[dict]) -> dict:
    servicio_ids = list({v["servicio_id"] for v in viajes})
    tarjeta_ids = list({v["tarjeta_id"] for v in viajes})
    paradero_ids = set()
    for v in viajes:
        paradero_ids.add(v["paradero_origen_id"])
        if v.get("paradero_final_id"):
            paradero_ids.add(v["paradero_final_id"])

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

    return {
        "servicios": servicios_por_id,
        "tarjetas": tarjetas_por_id,
        "paraderos": paraderos_por_id,
        "rutas": rutas_por_id
    }

def _enriquecer_viaje(v: dict, mapas: dict) -> dict:
    servicio = mapas["servicios"].get(v["servicio_id"])
    ruta = mapas["rutas"].get(servicio["ruta_id"]) if servicio else None
    tarjeta = mapas["tarjetas"].get(v["tarjeta_id"])
    paradero_origen = mapas["paraderos"].get(v["paradero_origen_id"])
    paradero_final = mapas["paraderos"].get(v.get("paradero_final_id"))

    return {
        "id": v["id"],
        "fecha_hora": v["fecha_hora"],
        "ruta_nombre": ruta["nombre"] if ruta else None,
        "tipo_servicio": ruta["tipo_servicio"] if ruta else None,
        "tarjeta_tipo": tarjeta["tipo"] if tarjeta else None,
        "paradero_origen_nombre": paradero_origen["nombre"] if paradero_origen else None,
        "paradero_final_nombre": paradero_final["nombre"] if paradero_final else None,
        "estado": v["estado"]
    }

async def obtener_historial(pasajero_id: int) -> dict:
    pasajero, viajes, conexiones = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id),
        ms3_client.obtener_conexiones_por_pasajero(pasajero_id)
    )
    mapas = await _resolver_relacionados(viajes)

    viajes_enriquecidos = [_enriquecer_viaje(v, mapas) for v in viajes]
    conexiones_enriquecidas = [
        {
            "id": c["id"],
            "viaje_origen_id": c["viaje_origen_id"],
            "viaje_destino_id": c["viaje_destino_id"],
            "paradero_nombre": mapas["paraderos"].get(c["paradero_id"], {}).get("nombre"),
            "fecha_hora": c["fecha_hora"]
        }
        for c in conexiones
    ]

    return {
        "pasajero_id": pasajero["id"],
        "nombre": pasajero["nombre"],
        "viajes": viajes_enriquecidos,
        "conexiones": conexiones_enriquecidas
    }

async def obtener_viajes(pasajero_id: int) -> dict:
    pasajero, viajes = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id)
    )
    mapas = await _resolver_relacionados(viajes)
    viajes_enriquecidos = [_enriquecer_viaje(v, mapas) for v in viajes]

    return {"pasajero_id": pasajero["id"], "viajes": viajes_enriquecidos}

async def obtener_resumen(pasajero_id: int) -> dict:
    pasajero, viajes, conexiones = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id),
        ms3_client.obtener_conexiones_por_pasajero(pasajero_id)
    )
    mapas = await _resolver_relacionados(viajes)
    viajes_enriquecidos = [_enriquecer_viaje(v, mapas) for v in viajes]

    conteo_tipo: dict[str, int] = {}
    for v in viajes_enriquecidos:
        if v["tipo_servicio"]:
            conteo_tipo[v["tipo_servicio"]] = conteo_tipo.get(v["tipo_servicio"], 0) + 1
    tipo_mas_usado = max(conteo_tipo, key=conteo_tipo.get) if conteo_tipo else None

    ultimo_viaje = max((v["fecha_hora"] for v in viajes), default=None)

    return {
        "pasajero_id": pasajero["id"],
        "total_viajes": len(viajes),
        "total_conexiones": len(conexiones),
        "tipo_servicio_mas_usado": tipo_mas_usado,
        "ultimo_viaje": ultimo_viaje
    }

async def obtener_tarjetas(pasajero_id: int) -> dict:
    pasajero, tarjetas, viajes = await asyncio.gather(
        ms1_client.obtener_pasajero(pasajero_id),
        ms1_client.obtener_tarjetas_por_pasajero(pasajero_id),
        ms3_client.obtener_viajes_por_pasajero(pasajero_id)
    )

    conteo_uso: dict[int, int] = {}
    for v in viajes:
        conteo_uso[v["tarjeta_id"]] = conteo_uso.get(v["tarjeta_id"], 0) + 1

    tarjetas_con_uso = [
        {
            "id": t["id"],
            "tipo": t["tipo"],
            "saldo": t["saldo"],
            "veces_usada": conteo_uso.get(t["id"], 0)
        }
        for t in tarjetas
    ]

    return {"pasajero_id": pasajero["id"], "tarjetas": tarjetas_con_uso}