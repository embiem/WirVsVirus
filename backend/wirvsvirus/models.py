
from enum import Enum
from typing import List, Optional, Union, Dict, Tuple

from pydantic import BaseModel

from wirvsvirus import db


class ProfileTypeEnum(str, Enum):
    """Capabailty a helper can have."""
    hospital = 'hospital'
    helper = 'helper'


class MatchStatus(str, Enum):
    """Match status."""
    pending = 'Pending'
    declined = 'Declined'
    accepted = 'Accepted'


class RoleEnum(str, Enum):
    """Capabailty a helper can have."""
    admin = 'admin'
    logistic = 'logistic'
    medical = 'medical'


class Location(db.MongoModel):
    type: str
    coordinates: Tuple[int, int]


class ProfileBase(db.MongoModel):
    """Basic profile with authentication info.

    The user_id is taken from the access token provided by our oauth provider
    (auth0).
    """
    email: str
    profile_type: ProfileTypeEnum

class ProfileInput(ProfileBase):
    """Model for the profile signup form.

    If you are a helper, you would fill the "helper" field.
    If your a hospital, you would fill the hospital id.
    """
    helper: Optional['HelperBase'] = None
    hospital_id: Optional[str] = None

class ProfileIntermediate(ProfileBase):
    """Profile with user id."""
    user_id: str  # provided by auth0
    helper_id: Optional[str] = None
    hospital_id: Optional[str] = None

class Profile(ProfileIntermediate):
    id: str

class PersonnelRequirementBase(db.MongoModel):
    """Personnel requirement for help."""
    hospital_id: str
    activity_id: str
    value: int = 1


class PersonnelRequirement(PersonnelRequirementBase):
    """Personnel requirement for help."""
    id: str = None


class MatchBase(db.MongoModel):
    """Match model."""
    helper_id: str
    personnel_requirement_id: str
    start_date: str
    end_date: str
    status: str
    info_text: str


class Match(MatchBase):
    """Match model."""
    id: str


class HelperBase(db.MongoModel):
    """Define helper model."""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    vaccination: Optional[str]
    housing_situation: Optional[str]

    zip_code: Optional[str]
    street: Optional[str]
    location: Optional[Location] = None

    # Qualifications managed in frontend and stored in db as strings.
    qualification_id: str
    work_experience_in_years: int

    # Activities managed in frontend. IDs stored as strings in DB
    activity_ids: List[str]


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
    personnel_requirement_ids: List[str] = []

    location: Optional[Location] = None
    healthcare_speciality: Optional[str]

    operator: Optional[str]
    operator_type: Optional[str]
    contact_phone: Optional[str]
    contact_website: Optional[str]
    contact_email: Optional[str]
    contact_fax: Optional[str]
    addr: Optional[str]
    address_full: Optional[str]
    address_street: Optional[str]
    address_housenumber: Optional[str]
    address_city: Optional[str]
    address_suburb: Optional[str]
    address_subdistrict: Optional[str]
    address_district: Optional[str]
    address_province: Optional[str]
    address_state: Optional[str]
    denomination: Optional[str]
    religion: Optional[str]
    emergency: Optional[str]
    rooms: Optional[str]
    beds: Optional[str]
    capacity: Optional[str]
    wheelchair: Optional[str]
    wikidata: Optional[str]
    wikipedia: Optional[str]
    orig_fid: Optional[str]
    globalid: Optional[str]


class Hospital(HospitalBase):
    id: str


class Proposition(db.MongoModel):
    hospital_id: str
    helper_ids: List[str]


class MatchProposition(db.MongoModel):
    allocations: List[Proposition]


ProfileInput.update_forward_refs()
