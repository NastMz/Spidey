from geopy.geocoders import Nominatim


def get_country_coordinates(country_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(country_name)
    if location:
        return location.latitude, location.longitude
    else:
        print(f"No se encontraron coordenadas para el país: {country_name}")
        return None
