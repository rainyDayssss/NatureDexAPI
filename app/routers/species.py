import httpx
import os
from urllib.parse import quote
from fastapi import APIRouter, UploadFile, HTTPException, File
from gradio_client import Client, handle_file
from app.schemas.species import SpeciesBase
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/api/species", tags=["Species"])

# Hugging Face Plant Classifier
hf_client = Client("juppy44/plant-classification")

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.1))
WIKI_BASE_URL = os.getenv("WIKI_BASE_URL")
INATURALIST_BASE_URL = os.getenv("INATURALIST_BASE_URL")

headers = {
    "User-Agent": os.getenv("USER_AGENT")
}


@router.post("/identify", response_model=SpeciesBase)
async def identify_and_enrich(image: UploadFile = File(...)):

    # -------------------------------
    # PHASE 1: Hugging Face Classification
    # -------------------------------
    temp_file = "temp_input_image.jpg"

    try:
        image_bytes = await image.read()
        with open(temp_file, "wb") as f:
            f.write(image_bytes)

        result = hf_client.predict(
            image=handle_file(temp_file),
            top_k=1,
            use_wa_adapter=False,
            api_name="/classify_plant"
        )

        scientific_name = result.get("label")
        confidence = result.get("confidences", [{}])[0].get("confidence", 0.0)

        if not scientific_name or confidence < CONFIDENCE_THRESHOLD:
            return {
                "scientific_name": "Unknown",
                "common_name": "Unknown",
                "description": "No plant species detected with sufficient confidence."
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model Prediction Error: {str(e)}")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # TODO: Add caching layer here to store previous results and avoid redundant API calls.
    # So check if species data already exists in the database before proceeding to enrichment.

    # -------------------------------
    # PHASE 2: Enrichment (iNaturalist + MediaWiki)
    # -------------------------------
    async with httpx.AsyncClient(timeout=10) as client:

        # ---- iNaturalist (common name only)
        search_url = f"{INATURALIST_BASE_URL}?q={quote(scientific_name)}&rank=species"
        inat_res = await client.get(search_url)

        if inat_res.status_code != 200:
            raise HTTPException(status_code=502, detail="iNaturalist API unavailable")

        results = inat_res.json().get("results", [])
        common_name = results[0].get("preferred_common_name") if results else None
        # TODO: Further enrichment can be added here, such as observation counts, images, etc.
        # TODO: Thus also update species models/schemas accordingly.

        # ---- MediaWiki (description)
        wiki_url = (
            f"{WIKI_BASE_URL}"
            "?action=query"
            "&format=json"
            "&prop=extracts"
            "&exintro=1"
            "&explaintext=1"
            "&redirects=1"
            f"&titles={quote(scientific_name)}"
        )

        wiki_res = await client.get(wiki_url, headers=headers)
        print(wiki_res)
        description = "No description available."
        if wiki_res.status_code == 200:
            wiki_json = wiki_res.json()
            pages = wiki_json.get("query", {}).get("pages", {})

            if pages:
                # Get the first page in the dict
                page = next(iter(pages.values()))

                # If page exists (not missing) use extract
                if not page.get("missing"):
                    description = page.get("extract", description)

    # TODO: Store spcecies data in the database for future retrieval.

    # -------------------------------
    # PHASE 3: Unified Response
    # -------------------------------
    return {
        "scientific_name": scientific_name,
        "common_name": common_name or scientific_name,
        "description": description
    }
