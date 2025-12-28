from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class UserCollectionsBase(BaseModel):
    profile_id: UUID
    species_id: UUID
    species_pic_path: str
    date_collected: datetime

class UserCollectionsCreate(UserCollectionsBase):
    pass

class UserCollectionsRead(UserCollectionsBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
