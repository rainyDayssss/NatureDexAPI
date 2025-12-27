from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CollectionsBase(BaseModel):
    profile_id: UUID
    species_id: UUID
    species_pic_path: str
    date_collected: datetime

class CollectionsCreate(CollectionsBase):
    pass

class CollectionsRead(CollectionsBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
