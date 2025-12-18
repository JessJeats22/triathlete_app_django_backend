import requests
import gpxpy
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two lat/lon points in meters.
    """
    R = 6371000  # Earth radius in meters

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def extract_gpx_metrics(gpx_url: str) -> dict:
    """
    Download a GPX file and return distance (km) and elevation gain (m).
    """

    response = requests.get(gpx_url, timeout=10)
    response.raise_for_status()

    gpx = gpxpy.parse(response.text)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(segment.points)

    if len(points) < 2:
        return {}

    total_distance = 0.0
    elevation_gain = 0.0

    for i in range(1, len(points)):
        p1 = points[i - 1]
        p2 = points[i]

        total_distance += haversine(
            p1.latitude, p1.longitude,
            p2.latitude, p2.longitude
        )

        if p1.elevation is not None and p2.elevation is not None:
            delta = p2.elevation - p1.elevation
            if delta > 0:
                elevation_gain += delta

    return {
        "distance_km": round(total_distance / 1000, 2),
        "elevation_gain": round(elevation_gain),
    }
