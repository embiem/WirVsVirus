"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI(
    title="WirVsVirus", description="WirVsVirus!"
)


class RoleEnum(str, Enum):
    """Capabailty a helper can have."""
    admin = 'admin'
    logistic = 'logistic'
    medical = 'medical'


class CapabilityEnum(str, Enum):
    """Capabailty a helper can have."""
    hotline = 'hotline'
    testing = 'testing'
    care_normal = 'care_normal'
    care_intensive = 'care_intensive'
    care_intensive_medical = 'care_intensive_medical'
    care_intensive_medical_ventilation = 'care_intensive_medical_ventilation'
    medical_specialist = 'medical_specialist'


class Address(BaseModel):
    """Adress schema."""
    id: UUID
    zip_code: int
    street: str
    latitude: float
    longitude: float


class Helper(BaseModel):
    """Define helper model."""
    id: UUID
    name: str
    email: EmailStr
    address: Address
    phone_number: str
    capability: CapabilityEnum
    helping_category: RoleEnum


class Hospital(BaseModel):
    """Hospital model."""
    id: UUID
    name: str
    address: dict
    website: Optional[HttpUrl]
    phone_number: Optional[str]


class User(BaseModel):
    """User model."""
    id: UUID
    email: EmailStr
    hospital_id: UUID


class HelperDemand(BaseModel):
    """Demand for help."""
    id: UUID
    hospital_id: UUID
    capability: CapabilityEnum
    value: int = 1


class Match(BaseModel):
    """Match model."""
    id: UUID
    helper_id: UUID
    demand_id: UUID
    helper_confirmed: bool = False
    hospital_confirmed: bool = False


@app.get('/matches', response_model=Match)
async def get_matches():
    """Retrieve matches."""
    pass


@app.post('/matches')
async def post_match(match: Match):
    """Post match."""
    pass


@app.post('/demand')
async def post_demand(demand: HelperDemand):
    """Post new demand."""
    pass


@app.post('/helpers')
async def post_helper(helper: Helper):
    """ Post helper."""
    pass