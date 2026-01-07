# 🌿 NatureDexAPI

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

NatureDexAPI is a **plant identification API** for the NatureDex app. Upload a photo, and it returns the **scientific name, common name, and description** of the plant using Hugging Face, iNaturalist, and Wikipedia.

---

## Features

- Identify plants from images with Hugging Face’s model  
- Enrich species data with **iNaturalist** and **Wikipedia**  
- Confidence thresholding for reliable results  

---

## Quick Start

1. Clone and install dependencies:

```bash
git clone https://github.com/yourusername/NatureDexAPI.git
cd NatureDexAPI
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt

2. Add a .env file with:

CONFIDENCE_THRESHOLD=0.1
USER_AGENT=NatureDexApp/1.0
WIKI_BASE_URL=https://en.wikipedia.org/w/api.php
INATURALIST_BASE_URL=https://api.inaturalist.org/v1/taxa

3. Run the API:

uvicorn app.main:app --reload

4. Access Swagger docs:

Access Swagger docs:


Usage

POST an image to /api/species/identify and get:

{
  "scientific_name": "Helianthus annuus",
  "common_name": "Common sunflower",
  "description": "The common sunflower (Helianthus annuus) is a species of large annual forb..."
}


License

MIT © 2026 [Jhon Rosell B. Talisic]