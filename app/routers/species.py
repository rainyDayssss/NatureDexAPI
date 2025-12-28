import httpx
# Use the FastAPI HTTPException, not the http.client one!
from fastapi import APIRouter, UploadFile, HTTPException, File
from typing import List
from uuid import UUID
from app.services.classifier import predict_species
from app.schemas.species import SpeciesBase, SpeciesCreate, SpeciesRead

router = APIRouter(prefix="/api/species", tags=["Species"])

@router.post("/identify", response_model=SpeciesBase)
async def identify_and_enrich(file: UploadFile = File(...)):
    # --- PHASE 1: LOCAL MODEL ---
    # Run your .tflite model on the uploaded image
    # Let's say it returns: "Pithecophaga jefferyi"
    pred = predict_species(await file.read())
    scientific_name = pred["species"]
    # confidence = pred["confidence"]

    # --- PHASE 2.A: LOCAL DATABASE ---
    # Check if the species is already in your species database
    # If it is, return the cached data
    # If not, proceed to Phase 2.B

    # --- PHASE 2.B: EXTERNAL API (iNaturalist) ---
    async with httpx.AsyncClient() as client: # OPEN the client
        # Step A: Search for ID
        search_url = f"https://api.inaturalist.org/v1/taxa?q={scientific_name}&rank=species"
        search_response = await client.get(search_url)
        
        if search_response.status_code != 200:
            raise HTTPException(status_code=502, detail="iNaturalist Search API unavailable")
        
        search_data = search_response.json()
        results = search_data.get('results', [])

        if not results:
            return {
                "scientific_name": scientific_name,
                "common_name": "Unknown Species",
                "description": "No species found in the database."
            }

        # Step B: Get Full Details (Keep this inside the 'async with' block!)
        taxon_id = results[0]['id']
        detail_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}"
        detail_res = await client.get(detail_url)
        
        if detail_res.status_code != 200:
            raise HTTPException(status_code=502, detail="iNaturalist Detail API unavailable")
            
        detail_data = detail_res.json()
        taxon = detail_data.get('results', [{}])[0]

    # --- PHASE 3: RETURN DATA ---
    return {
        "scientific_name": scientific_name,
        "common_name": taxon.get('preferred_common_name', scientific_name),
        "description": taxon.get('wikipedia_summary') or "Summary currently unavailable."
    }

