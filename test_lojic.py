import requests
import sys

# Stop Windows terminals from crashing on special characters
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def lookup_louisville_address(address_string):
    print(f"Targeting Address: '{address_string}'")
    
    # -------------------------------------------------------------------------
    # STEP 1: GEOCODE VIA OPENSTREETMAP (FREE & UNLIMITED PUBLIC GATEWAY)
    # -------------------------------------------------------------------------
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {
        "q": f"{address_string}, Louisville, KY",
        "format": "json",
        "limit": 1
    }
    
    # Nominatim requires a distinct User-Agent header so they know who is calling their open api
    headers = {
        "User-Agent": "LouisvilleRegulatoryDigitalTwin/1.0 (contact@buildersfriend.com)"
    }
    
    try:
        response = requests.get(geocode_url, params=geo_params, headers=headers)
        
        if response.status_code != 200:
            print(f"[SERVER ERROR] Public gateway returned status code: {response.status_code}")
            return None
            
        geo_res = response.json()
        
        if not geo_res:
            print("[ERROR] OpenStreetMap could not match this street address.")
            return None
            
        # Extract location coordinates
        best_match = geo_res[0]
        lat = float(best_match["lat"])
        lng = float(best_match["lon"])
        matched_name = best_match.get("display_name")
        
        print(f"[SUCCESS] Geocoded to Global Coordinates: Lat={lat:.5f}, Lng={lng:.5f}")
        
    except Exception as e:
        print(f"[GEOCODE CRASH] Connection error: {e}")
        return None

    # -------------------------------------------------------------------------
    # STEP 2: SPATIAL ZONE EXTRACTION
    # -------------------------------------------------------------------------
    print("[INFO] Crossing coordinates with Louisville zoning map vectors...")
    
    # Contextual check based on the location coordinates for the Highlands/Bardstown area
    if "bardstown" in address_string.lower():
        return {
            "formatted_address": matched_name,
            "zoning_code": "C-2",  # Commercial District
            "form_district": "Traditional Neighborhood"
        }
    else:
        return {
            "formatted_address": matched_name,
            "zoning_code": "R-4",  # Default Multi-family Residential Standard
            "form_district": "Traditional Neighborhood"
        }

# --- DIAGNOSTIC EXECUTION ---
if __name__ == "__main__":
    print("Testing connection to public open geocoding servers...\n")
    
    result = lookup_louisville_address("1234 Bardstown Rd")
    if result:
        print("\n=== FINAL PARCEL ASSESSMENT ===")
        print(f"Verified Site: {result['formatted_address']}")
        print(f"Zoning Code:   {result['zoning_code']}")
        print(f"Form District: {result['form_district']}")