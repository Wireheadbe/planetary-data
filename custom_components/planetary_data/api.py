import requests

URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

def fetch_k_index():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError("No K-index data returned")
    return data[-1]
