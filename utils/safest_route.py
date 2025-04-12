
import openrouteservice
from openrouteservice import convert
import numpy as np

client = openrouteservice.Client(key="5b3ce3597851110001cf62482f2a1238cdbc419bad579203d50c08da")  # Replace with your API key

def get_route_coordinates(source, destination):
    coords = (source, destination)
    res = client.directions(coords, profile='foot-walking', format='geojson')
    route = res['features'][0]['geometry']['coordinates']
    return [[point[1], point[0]] for point in route]  # lon,lat -> lat,lon

def score_route(route_coords, crime_df):
    nearby_crimes = 0
    for point in route_coords:
        for _, row in crime_df.iterrows():
            dist = np.sqrt((point[0] - row['latitude'])**2 + (point[1] - row['longitude'])**2)
            if dist < 0.005:
                nearby_crimes += 1
    return max(0, 100 - nearby_crimes * 10)

def get_color(score):
    if score > 80:
        return 'green'
    elif score > 60:
        return 'yellow'
    else:
        return 'red'

def get_safest_route_from_coords(source, destination, crime_df):
    route_coords = get_route_coordinates(source, destination)
    score = score_route(route_coords, crime_df)
    center = route_coords[len(route_coords) // 2]
    return {"route": route_coords, "score": score, "center": center}
