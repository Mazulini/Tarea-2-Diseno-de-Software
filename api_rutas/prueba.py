import csv
import requests
import json
import folium
from folium.features import DivIcon
from polyline import decode
import webbrowser
import time
from datetime import timedelta
from haversine import haversine
import os

API_KEY = "AIzaSyCnjHg35KqeitpjSTUwL76p9OhfBadwg0M"
GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
}

def es_coordenada(linea):
    partes = linea.split(',')
    if len(partes) != 2:
        return False
    try:
        float(partes[0].strip())
        float(partes[1].strip())
        return True
    except ValueError:
        return False

def geocodificar_direccion(direccion):
    GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": direccion,
        "key": API_KEY
    }
    response = requests.get(GEOCODING_URL, params=params)
    response.raise_for_status()
    resultados = response.json().get("results")
    if not resultados:
        raise ValueError(f"No se pudo geocodificar la dirección: {direccion}")
    location = resultados[0]["geometry"]["location"]
    time.sleep(0.1)  # para no saturar la API
    return [location["lat"], location["lng"]]

def leer_coordenadas_desde_csv(archivo_csv):
    puntos = []

    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        lineas = [line.strip() for line in file if line.strip()]
    
    if not lineas:
        raise ValueError("El archivo CSV está vacío.")

    if es_coordenada(lineas[0]):
        for line in lineas:
            lat_str, lon_str = line.replace('"', '').replace("'", "").split(',')
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            puntos.append([lat, lon])
    else:
        for direccion in lineas:
            coord = geocodificar_direccion(direccion)
            puntos.append(coord)

    if len(puntos) < 2:
        raise ValueError("El archivo debe contener al menos 2 puntos (origen y destino).")

    origen = puntos[0]
    destino = puntos[-1]
    waypoints = puntos[1:-1] if len(puntos) > 2 else []
    return origen, destino, waypoints

def punto_a_dict(punto):
    return {"latitude": punto[0], "longitude": punto[1]}

def construir_payload(origen, destino, waypoints, travel_mode="DRIVE"):
    payload = {
        "origin": {"location": {"latLng": punto_a_dict(origen)}},
        "destination": {"location": {"latLng": punto_a_dict(destino)}},
        "travelMode": travel_mode,
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
    }
    if waypoints:
        payload["intermediates"] = [{"location": {"latLng": punto_a_dict(wp)}} for wp in waypoints]
    return payload

def solicitar_ruta(payload):
    response = requests.post(GOOGLE_ROUTES_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["routes"][0]

def decodificar_polyline(encoded_polyline):
    return decode(encoded_polyline)

def agregar_info_html(mapa, duracion_segundos, distancia_metros):
    if isinstance(duracion_segundos, str):
        duracion_segundos = int(duracion_segundos.replace("s", "").strip())
    else:
        duracion_segundos = int(duracion_segundos)
    
    duracion_timedelta = timedelta(seconds=duracion_segundos)
    distancia_km = distancia_metros / 1000
    info_html = f"""
    <div id="info-ruta" style='position: fixed; bottom: 50px; left: 50px; z-index: 9999; background-color: white;
        padding: 15px; border: 2px solid black; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0,0,0,0.3);'>
        <h4>Información de la Ruta</h4>
        <b>Duración:</b> {str(duracion_timedelta)}<br>
        <b>Distancia:</b> {distancia_km:.2f} km<br>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(info_html))

def crear_mapa(origen, destino, waypoints, coordenadas_ruta, color_ruta, duracion_segundos, distancia_metros):
    mapa = folium.Map(location=origen, zoom_start=13)

    # Preparamos lista completa y colores
    puntos = [origen] + waypoints + [destino]
    colores = ['green'] + ['blue'] * len(waypoints) + ['red']

    # Marcadores numerados con estilo personalizado
    for i, punto in enumerate(puntos):
        folium.Marker(
            location=punto,
            icon=DivIcon(
                icon_size=(30, 30),
                icon_anchor=(15, 15),
                html=f"""
                <div style="
                    background-color: {colores[i]};
                    color: white;
                    border-radius: 50%;
                    text-align: center;
                    font-size: 16px;
                    font-weight: bold;
                    width: 30px;
                    height: 30px;
                    line-height: 30px;
                    border: 2px solid black;
                    box-shadow: 1px 1px 5px rgba(0,0,0,0.5);
                    cursor: pointer;">
                    {i + 1}
                </div>
                """
            )
        ).add_to(mapa)

    # Dibujar ruta
    folium.PolyLine(coordenadas_ruta, color=color_ruta, weight=6, opacity=0.7).add_to(mapa)

    # Agregar info de duración y distancia
    agregar_info_html(mapa, duracion_segundos, distancia_metros)

    archivo_html = "mapa_ruta.html"
    mapa.save(archivo_html)
    print(f"Mapa guardado en {archivo_html}")
    
    url_absoluta = f"file://{os.path.abspath(archivo_html)}"
    webbrowser.open(url_absoluta)

def main():
    archivo_csv = "api_rutas/direcciones.csv"  
    origen, destino, waypoints = leer_coordenadas_desde_csv(archivo_csv)

    payload = construir_payload(origen, destino, waypoints, travel_mode="DRIVE")
    ruta = solicitar_ruta(payload)

    duracion = ruta["duration"]
    distancia = ruta["distanceMeters"]
    polyline_encoded = ruta["polyline"]["encodedPolyline"]
    coordenadas_ruta = decodificar_polyline(polyline_encoded)

    crear_mapa(origen, destino, waypoints, coordenadas_ruta, "blue", duracion, distancia)

if __name__ == "__main__":
    main()
