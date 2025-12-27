from uuid import UUID
from pydantic import BaseModel, ConfigDict

class SpeciesBase(BaseModel):
    common_name: str
    scientific_name: str
    description: str

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesRead(SpeciesBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
