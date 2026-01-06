import httpx
from fastapi import APIRouter, UploadFile, HTTPException, File
from gradio_client import Client, handle_file
from app.schemas.species import SpeciesBase

router = APIRouter(prefix="/api/species", tags=["Species"])

# Initialize once (not inside the function to save startup time)
hf_client = Client("juppy44/plant-classification")

@router.post("/identify", response_model=SpeciesBase)
async def identify_and_enrich(image: UploadFile = File(...)):

    # -----------------------------------
    # PHASE 1: Hugging Face Inference
    # -----------------------------------
    try:
        # Save uploaded image temporarily for handle_file
        image_bytes = await image.read()
        temp_file = "temp_input_image.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_bytes)

        # HF Prediction
        result = hf_client.predict(
            image=handle_file(temp_file),
            top_k=1, # the top 1 species
            use_wa_adapter=False,
            api_name="/classify_plant"
        )

        scientific_name = result.get("label")
        confidence = result.get("confidences", [{}])[0].get("confidence", 0.0)

        # ------------------------------
        #  PHASE 1B: Confidence Threshold
        # ------------------------------

        THRESHOLD = 0.1 # adjustable threshold
        if confidence < THRESHOLD:
            return {
                "scientific_name": "Unknown",
                "common_name": "Unknown",
                "description": "No plant species detected with sufficient confidence."
            }
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model Prediction Error: {str(e)}")

    

    if not scientific_name:
        raise HTTPException(status_code=400, detail="No plant species detected in the image.")

    # Plan to check if scientific_name already existed in database supabase

    # -----------------------------------
    # PHASE 2: Enrich with iNaturalist API
    # -----------------------------------
    async with httpx.AsyncClient() as client:
        # Step A: Search for taxon ID
        search_url = f"https://api.inaturalist.org/v1/taxa?q={scientific_name}&rank=species"
        search_res = await client.get(search_url)

        if search_res.status_code != 200:
            raise HTTPException(status_code=502, detail="iNaturalist Search API unavailable")

        results = search_res.json().get("results", [])
        if not results:
            return {
                "scientific_name": scientific_name,
                "common_name": "Unknown",
                "description": "No species found in the database"
            }

        taxon_id = results[0]["id"]

        # Step B: Fetch full species details
        detail_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}"
        detail_res = await client.get(detail_url)

        if detail_res.status_code != 200:
            raise HTTPException(status_code=502, detail="iNaturalist Detail API unavailable")

        detail_data = detail_res.json().get("results", [{}])[0]

    # -----------------------------------
    # PHASE 3: Return unified response
    # -----------------------------------
    return {
        "scientific_name": scientific_name,
        "common_name": detail_data.get("preferred_common_name", scientific_name),
        "description": detail_data.get("wikipedia_summary") or "No summary available."
    }
