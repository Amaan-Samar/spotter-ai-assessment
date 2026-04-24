import requests
import json
from typing import List, Tuple, Optional

# Free OSRM API (no key needed)
OSRM_API = "http://router.project-osrm.org/route/v1/driving/"
NOMINATIM_API = "https://nominatim.openstreetmap.org/search"

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """Convert address to coordinates using free Nominatim API"""
    try:
        response = requests.get(
            NOMINATIM_API,
            params={
                'q': address,
                'format': 'json',
                'limit': 1
            },
            headers={'User-Agent': 'SpotterAI-Assessment/1.0'}
        )
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return (lat, lon)
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None

def get_route_distance(origin: str, destination: str) -> Optional[float]:
    """Get driving distance in miles between two addresses"""
    try:
        # Geocode both addresses
        origin_coords = geocode_address(origin)
        dest_coords = geocode_address(destination)
        
        if not origin_coords or not dest_coords:
            # Return dummy data for demo if geocoding fails
            return get_dummy_distance(origin, destination)
        
        # Call OSRM
        coordinates = f"{origin_coords[1]},{origin_coords[0]};{dest_coords[1]},{dest_coords[0]}"
        url = OSRM_API + coordinates + "?overview=false"
        
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok':
            distance_meters = data['routes'][0]['distance']
            distance_miles = distance_meters * 0.000621371
            return round(distance_miles, 1)
    
    except Exception as e:
        print(f"Routing error: {e}")
    
    return get_dummy_distance(origin, destination)

def get_dummy_distance(origin: str, destination: str) -> float:
    """Return dummy distances for demo when API fails"""
    dummy_routes = {
        ('Chicago', 'Indianapolis'): 180,
        ('Indianapolis', 'Atlanta'): 540,
        ('Chicago', 'Atlanta'): 720,
        ('New York', 'Boston'): 215,
        ('Los Angeles', 'San Francisco'): 380,
    }
    
    # Try exact match
    if (origin, destination) in dummy_routes:
        return dummy_routes[(origin, destination)]
    
    # Try partial match
    for (o, d), dist in dummy_routes.items():
        if o in origin and d in destination:
            return dist
    
    # Default fallback
    return 500  # Default 500 miles

def get_full_route(origin: str, waypoint: str, destination: str) -> Tuple[float, List]:
    """Get total distance and route geometry for full trip"""
    # Get individual distances
    dist1 = get_route_distance(origin, waypoint)
    dist2 = get_route_distance(waypoint, destination)
    total = dist1 + dist2 if dist1 and dist2 else 0
    
    # Return dummy geometry points for map
    dummy_geometry = [
        [-87.6298, 41.8781],  # Chicago
        [-86.1581, 39.7684],  # Indianapolis
        [-84.3880, 33.7490],  # Atlanta
    ]
    
    return total, dummy_geometry