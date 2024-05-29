import json

# Diccionario de coordenadas
coordinates_dict = {
    'Chile': (-31.7613365, -71.3187697),
    'France': (46.603354, 1.8883335),
    'United States': (39.7837304, -100.445882),
    'Thailand': (7.4931858, 124.724704),
    'Brasil': (-10.3333333, -53.2),
    'Germany': (51.1638175, 10.4478313),
    'New Zealand': (-41.5000831, 172.8344077),
    'Australia': (-24.7761086, 134.755),
    'United Kingdom': (54.7023545, -3.2765753),
    'Spain': (39.3260685, -4.8379791),
    'Colombia': (4.099917, -72.9088133),
    'Japan': (36.5748441, 139.2394179),
    'Canada': (61.0666922, -107.991707),
    'China': (35.000074, 104.999927),
    'Singapore': (1.357107, 103.8194992)
}

# Convertir el diccionario en una lista de diccionarios
coordinates_list = [{'country': country, 'coords': coords} for country, coords in coordinates_dict.items()]

# Convertir la lista de diccionarios a una cadena JSON
coordinates_json = json.dumps(coordinates_list, indent=4)

# Imprimir el JSON resultante
print(coordinates_json)
