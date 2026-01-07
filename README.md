🌿 NatureDexAPI






NatureDexAPI is a plant identification API for the NatureDex app. Upload a photo, and it returns the scientific name, common name, and description of the plant using Hugging Face, iNaturalist, and Wikipedia.

Features

Identify plants from images with Hugging Face’s model

Enrich species data with iNaturalist and Wikipedia

Confidence thresholding for more reliable results

Quick Start

Clone and install dependencies:

git clone https://github.com/yourusername/NatureDexAPI.git
cd NatureDexAPI
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Add .env file with:

CONFIDENCE_THRESHOLD=0.1
USER_AGENT=NatureDexApp/1.0
WIKI_BASE_URL=https://en.wikipedia.org/w/api.php
INATURALIST_BASE_URL=https://api.inaturalist.org/v1/taxa


Run the API:

uvicorn app.main:app --reload


Access Swagger docs:

http://127.0.0.1:8000/docs

Usage

POST an image to /api/species/identify and get:

{
  "scientific_name": "Helianthus annuus",
  "common_name": "Common sunflower",
  "description": "The common sunflower (Helianthus annuus) is a species of large annual forb..."
}

License

MIT © 2026 [Your Name]