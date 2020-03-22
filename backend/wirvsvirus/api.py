"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from wirvsvirus import db, models, auth, crud
from wirvsvirus.graphql import graphql_app
from wirvsvirus.matching import MatchingModel

app = FastAPI(
    title="WirVsVirus", description="WirVsVirus!"
)

app.add_event_handler("startup", db.connect)
app.add_event_handler("shutdown", db.disconnect)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/profile', response_model=models.Profile)
async def post_profile(profile: models.ProfileBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create your profile.

    This creates the currently authenticated users profile.
    After authenticating, we need to first create this profile before further actions can be taken.
    """
    profile = models.ProfileIntermediate(**profile.dict(), user_id=jwt_payload['sub'])
    db_profile = await db.profiles.find_one({'user_id': profile.user_id})
    if db_profile:
        raise HTTPException(409, detail='profile already exists!')
    return await crud.create_item('profiles', profile)

@app.get('/profile', response_model=models.Profile)
async def get_current_profile(db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Get current users profile"""
    profile = await db.profiles.find_one({'user_id': jwt_payload['sub']})
    if not profile:
        raise HTTPException(404, detail='No profile found')
    return profile

@app.post('/matches', response_model=models.Match)
async def create_match(match: models.MatchBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create match."""
    return await crud.create_item('matches', match)


@app.get('/matches/propositions')
async def propose_matches(db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Propose matches."""
    hospitals = await crud.find("hospitals", {}, {'name': 1, 'location': 1})
    for hospital in hospitals:
        requirements = await crud.find("personnel_requirements", {"hospital_id": str(hospital["_id"])})
        demand = {r["activity_id"]: r["value"] for r in requirements}
        hospital.update({'demand': demand})
    helpers = await crud.find("helpers", {}, {'id': 1, 'location': 1, 'activity_ids': 1})
    model = MatchingModel(
        hospitals=hospitals, worker=helpers
    )
    model.solve()
    return model.results["allocation"]


@app.post('/personnel_requirements', response_model=models.PersonnelRequirement)
async def create_personnel_requirements(personnel_requirement: models.PersonnelRequirementBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create new personnel requirement."""
    return await crud.create_item('personnel_requirements', personnel_requirement)

@app.post('/helpers', response_model=models.Helper)
async def create_helper(helper: models.HelperBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create helper."""
    return await crud.create_item('helpers', helper)

@app.post('/hospitals', response_model=models.Hospital)
async def create_hospital(hospital: models.HospitalBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Post match."""
    return await crud.create_item('hospitals', hospital)

app.add_route("/graphql", graphql_app)
