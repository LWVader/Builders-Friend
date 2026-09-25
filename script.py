import requests

def get_louisville_zoning(address):
    # Step A: Convert the street address into spatial coordinates (Geocoding)
    # Using LOJIC's composite locator service
    geocode_url = "https://loi.lojic.org/arcgis/rest/services/Composite_Address_Locator/GeocodeServer/findAddressCandidates"
    geo_params = {
        "SingleLine": address,
        "f": "json"
    }
    
    geo_res = requests.get(geocode_url, params=geo_params).json()
    if not geo_res.get("candidates"):
        return "Address not found"
        
    location = geo_res["candidates"][0]["location"]
    x, y = location["x"], location["y"] # State Plane or Web Mercator coordinates

    # Step B: Spatial Query LOJIC's Zoning Layer using those coordinates
    # Layer 0 is typically the active Zoning Districts layer
    zoning_url = "https://loi.lojic.org/arcgis/rest/services/Zoning/MapServer/0/query"
    zone_params = {
        "geometry": f"{x},{y}",
        "geometryType": "esriGeometryPoint",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "ZONING_CODE,FORM_DISTRICT",
        "f": "json"
    }
    
    zone_res = requests.get(zoning_url, params=zone_params).json()
    
    # Extract the zoning traits safely
    attributes = zone_res["features"][0]["attributes"]
    return {
        "zone": attributes.get("ZONING_CODE"),         # e.g., "R-4"
        "form_district": attributes.get("FORM_DISTRICT") # e.g., "Traditional Neighborhood"
    }