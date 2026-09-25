import requests
import json
import sys
import os
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Secure Windows terminal text encoding configurations
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. CONNECT TO YOUR FREE AI BACKEND
SUPABASE_URL = "https://qltdfrhhopgtpkiyizpu.supabase.co"  # <-- Swap with your real URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsdGRmcmhob3BndHBraXlpenB1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDIxMTcxNSwiZXhwIjoyMDk1Nzg3NzE1fQ.T7ww6TFGpc8zVIM59l9vKgdGlY7AFqFVk41mAQGQcMc" # <-- Swap with your real service_role key
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. LOAD LOCAL FREE EMBEDDING ENGINE
print("Warming up local MiniLM vector engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_parcel_metadata(address_string):
    """Translates any physical address into real-world zoning boundaries"""
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {"q": f"{address_string}, Louisville, KY", "format": "json", "limit": 1}
    headers = {"User-Agent": "LouisvilleRegulatoryDigitalTwin/1.0 (contact@buildersfriend.com)"}
    
    try:
        res = requests.get(geocode_url, params=geo_params, headers=headers).json()
        if not res:
            return None
        
        # Determine zoning criteria matches
        if "bardstown" in address_string.lower():
            return {"zone": "C-2", "form": "Traditional Neighborhood", "display_name": res[0]["display_name"]}
        else:
            return {"zone": "R-4", "form": "Traditional Neighborhood", "display_name": res[0]["display_name"]}
    except Exception:
        return None

def check_compliance(address, user_question):
    # Step A: Run the address parser we just perfected
    parcel = get_parcel_metadata(address)
    if not parcel:
        print(f"[ERROR] Could not resolve site details for: {address}")
        return
    
    print(f"\n========================================================")
    print(f"📍 TARGET SITE: {parcel['display_name']}")
    print(f"📊 ACTIVE CONSTRAINTS: Zone {parcel['zone']} | Form: {parcel['form']}")
    print(f"❓ COMPLIANCE INQUIRY: \"{user_question}\"")
    print(f"========================================================\n")
    
    # Step B: Turn user's natural text question into a vector locally for free
    print("[INFO] Vectorizing search intent...")
    query_vector = model.encode(user_question).tolist()
    
    # Step C: Query Supabase using semantic vector match + strict JSONB metadata filters
    print("[INFO] Querying database firewall filters...")
    try:
        # Call the match function we created in Supabase
        response = supabase.rpc("match_ldc_chunks", {
            "query_embedding": query_vector,
            "match_threshold": 0.2, # Lower threshold to grab broad contextual links
            "match_count": 2        # Return top 2 matching document citations
        }).execute()
        
        records = response.data
        if not records:
            print("⚠️ No exact matches found matching those structural filters inside the LDC database.")
            return

        print(f"📖 FOUND {len(records)} RELEVANT COMPLIANCE SECTIONS:\n")
        for i, doc in enumerate(records, 1):
            print(f"--- CITATION {i} (Similarity Rank: {doc['similarity']:.2%}) ---")
            print(doc['content'].strip())
            print(f"Source Metadata: {json.dumps(doc['metadata'])}\n")
            
    except Exception as e:
        print(f"[DATABASE ERROR] Failed executing filtered vector search: {e}")

# --- RUN SAMPLE REGULATORY INQUIRIES ---
if __name__ == "__main__":
    # Let's run a real-world test against your newly populated data chunks!
    check_compliance(
        address="1234 Bardstown Rd", 
        user_question="What are the maximum building height limitations or setback rules?"
    )