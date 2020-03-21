"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

import requests
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI(
    title="WirVsVirus", description="WirVsVirus!"
)


class HelpingEnum(str, Enum):
    """Capabailty a helper can have."""
    admin = 'admin'
    logistic = 'logistic'
    medical = 'medical'


class CapabilityEnum(str, Enum):
    """Capabailty a helper can have."""
    hotline = 'hotline'
    testing = 'testing'
    normal = 'normal'
    intensive = 'intensive'
    intensive_medication = 'intensive_medication'
    intensive_respiration = 'intensive_respiration'
    intensive_doc = 'intensive_doc'


class Helper(BaseModel):
    """Define helper model."""
    id: UUID
    name: str
    email: EmailStr
    address: str
    phone_number: str
    capability: CapabilityEnum
    helping_category: HelpingEnum


class Hospital(BaseModel):
    """Hospital model."""
    id: UUID
    name: str
    address: dict
    website: Optional[HttpUrl]
    phone_number: Optional[str]


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
