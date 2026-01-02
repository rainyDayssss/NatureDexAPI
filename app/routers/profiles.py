
from uuid import UUID
from fastapi import APIRouter
from app.schemas.profiles import ProfilesBase, ProfilesCreate, ProfilesRead

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])

# Get user profile
@router.get("/me", response_model=ProfilesRead)      
async def get_profile(user_id: UUID):
    pass

# Update user profile (think about using id or email based from the jwt)
@router.patch("/{user_id}", response_model=ProfilesBase)
async def update_profile(user_id: UUID, new_profile: ProfilesCreate):
    pass

