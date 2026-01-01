from fastapi import APIRouter
from app.schemas.profiles import ProfilesBase, ProfilesCreate

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])

profile_list = [
    ProfilesCreate(username="user1", bio="Bio of user1", profile_pic_path="/images/user1.jpg"),
    ProfilesCreate(username="user2", bio="Bio of user2", profile_pic_path="/images/user2.jpg"),
    ProfilesCreate(username="user3", bio="Bio of user3", profile_pic_path="/images/user3.jpg"),
    ]

# Path var
@router.get("/{profile_id}", response_model=ProfilesBase)
def GetProfile(profile_id: str):
    return {
        "username": profile_id,
        "bio": "This is a sample bio.",
        "profile_pic_path": "/images/sample.jpg"
    }

@router.get("",response_model=dict[str, list[ProfilesBase]])    
def GetAllProfiles():
    return {
        "profile_list": profile_list
    }

# Query param


# Req body

