from uuid import UUID
from pydantic import BaseModel, ConfigDict

class FollowsBase(BaseModel):
    follower_id: UUID
    followee_id: UUID

class FollowsCreate(FollowsBase):
    pass

class FollowsRead(FollowsBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID