"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from wirvsvirus import db, models, auth, crud
from wirvsvirus.graphql import graphql_app

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
async def post_match(profile: models.ProfileBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create your profile.

    This creates the currently authenticated users profile.
    After authenticating, we need to first create this profile before further actions can be taken.
    """
    profile = models.IntermediateProfile(**profile.dict(), user_id=jwt_payload['sub'])
    db_profile = db.get_database().profiles.find_one({'user_id': profile.user_id})
    if db_profile:
        raise HTTPException(409, detail='profile already exists!')
    return await crud.create_item('profiles', profile)

@app.post('/matches', response_model=models.Match)
async def post_match(match: models.MatchBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Post match."""
    return await crud.create_item('matches', match)

@app.post('/demands', response_model=models.HelperDemand)
async def post_demand(demand: models.HelperDemandBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Post new demand."""
    return await crud.create_item('demands', demand)

@app.post('/helpers', response_model=models.Helper)
async def post_helper(helper: models.HelperBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """ Post helper."""
    return await crud.create_item('helpers', helper)

@app.post('/hospitals', response_model=models.Hospital)
async def post_hospitals(hospital: models.HospitalBase, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Post match."""
    return await crud.create_item('hospitals', hospital)

app.add_route("/graphql", graphql_app)
