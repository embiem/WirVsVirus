"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import requests
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="WirVsVirus", description="WirVsVirus!"
)


class User(BaseModel):
    """Define user model."""

    id: UUID
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    user_type: str  # helper? or hospital?
    capabilities: 'HelperCapabilityProfile'  # help capabilities if this is a helper
    hospital_id: Optional[UUID]  # hospital id if this is a hospital user


class Hospital(BaseModel):
    """Hospital model?"""

    id: UUID
    name: str
    address: dict
    location: dict
    needs: dict  # what does this hospital need... TODO: the name "needs" is bad, we need something better.


class HelperCapabilityProfile(BaseModel):
    capabilities: List['Experience']
    qualifications: List['Qualification']
    address: dict
    radius: float  # km away from address this person could work?
    cohabitants: int  # number of cohabitants
    child_cohabitants: bool  # do children live with this helper
    # TODO: try and figure out how to model availability and when the helper is blocked by a hospital.
    availability: dict  # calendar data / or some sort of ranges / number of hours ?

class Experience(BaseModel):
    """Experience level for a specific capability."""
    capability_id: UUID
    level: int


class Qualification(BaseModel):
    """Document showing some sort of qualification (university degree or something)."""
    document: str


class Capability(BaseModel):
    """Capabailty a helper can have."""
    id: UUID
    name: str
    category: str  # medical, administrative, logistical?
    tags: List[str]  # random other search tearms or categories?


@app.get("/users")
async def read_users_me() -> List[User]:
    """Return the current user information."""
    return []
