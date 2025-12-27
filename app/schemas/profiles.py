from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ProfilesBase(BaseModel):
    username: str
    bio: Optional[str] = None
    profile_pic_path: Optional[str] = None

class ProfilesCreate(ProfilesBase):
    pass

class ProfilesRead(ProfilesBase):
    model_config = ConfigDict(from_attributes=True)
    level: int = 1
    exp: int = 0
    id: UUID
    
