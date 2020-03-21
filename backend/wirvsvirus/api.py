"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
import graphene
from graphene_pydantic import PydanticObjectType
from pydantic import BaseModel, EmailStr, HttpUrl
from starlette.graphql import GraphQLApp

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


class AddressModel(BaseModel):
    """Adress schema."""
    id: str
    zip_code: int
    street: str
    latitude: float
    longitude: float


class HelperModel(BaseModel):
    """Define helper model."""
    id: UUID
    name: str
    email: str
    address: str  # AddressModel
    phone_number: str
    capability: CapabilityEnum
    helping_category: RoleEnum


class HospitalModel(BaseModel):
    """Hospital model."""
    id: str
    name: str
    address: str
    website: Optional[str]
    phone_number: Optional[str]


class HelperDemandModel(BaseModel):
    """Demand for help."""
    id: str
    hospital_id: str
    capability: CapabilityEnum
    value: int = 1


class MatchModel(BaseModel):
    """Match model."""
    id: str
    helper_id: str
    demand_id: str
    helper_confirmed: bool = False
    hospital_confirmed: bool = False


class Helper(PydanticObjectType):
    class Meta:
        model = HelperModel


class HelperDemand(PydanticObjectType):
    class Meta:
        model = HelperDemandModel


class Hospital(PydanticObjectType):
    class Meta:
        model = HospitalModel


class Match(PydanticObjectType):
    class Meta:
        model = MatchModel


class Query(graphene.ObjectType):
    hospital = graphene.Field(Hospital, id=graphene.ID())

    def resolve_hospital(self, info, id):
        return HospitalModel(id=1, name='Maria Hospital', address='Straße')


@app.get('/matches', response_model=MatchModel)
async def get_matches():
    """Retrieve matches."""
    pass


@app.post('/matches')
async def post_match(match: MatchModel):
    """Post match."""
    pass


@app.post('/demand')
async def post_demand(demand: HelperDemandModel):
    """Post new demand."""
    pass


@app.post('/helpers')
async def post_helper(helper: HelperModel):
    """ Post helper."""
    pass


app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))
