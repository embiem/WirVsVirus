
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from wirvsvirus import db



class ProfileTypeEnum(str, Enum):
    """Capabailty a helper can have."""
    hospital = 'hospital'
    helper = 'helper'


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


class BaseProfile(db.MongoModel):
    """Basic profile with authentication info.

    The user_id is taken from the access token provided by our oauth provider
    (auth0).
    """
    email: str
    user_id: str  # provided by auth0


class Profile(db.MongoModel):
    id: str
    helper_id: str = None
    hospital_id: str = None

    @property
    def profile_type(self) -> Optional[ProfileTypeEnum]:
        if self.helper_id:
            return ProfileTypeEnum.hospital
        if self.hospital_id:
            return ProfileTypeEnum.hospital
        return None

class AddressBase(BaseModel):
    zip_code: str
    street: str
    latitude: float
    longitude: float


class HelperBase(db.MongoModel):
    """Define helper model."""
    name: str
    email: str
    address: str  # AddressModel
    X: float
    Y: float
    phone_number: str
    activities: List[str]  # List of acitvity ids
    qualification_name: str
    years: int
    vaccination: Optional[str]
    profile_id: Optional[str] = None


class Helper(HelperBase):
    """Define helper model."""
    id: str


class HospitalBase(db.MongoModel):
    """Hospital model."""
    name: str
    address: str
    website: Optional[str]
    phone_number: Optional[str]
    profile_id: Optional[str] = None
    helper_demand_ids: List[str] = []

class Hospital(HospitalBase):
    id: str


class RequestBase(db.MongoModel):
    """Demand for help."""
    hospital_id: str
    activity_id: str
    value: int = 1

class Request(RequestBase):
    """Demand for help."""
    id: str = None


class MatchBase(db.MongoModel):
    """Match model."""
    helper_id: str
    request_id: str
    request_status: ["Pending", "Declined", "Accepted"]

class Match(MatchBase):
    """Match model."""
    id: str
