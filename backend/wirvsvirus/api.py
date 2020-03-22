"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from uuid import UUID
from math import sqrt
import logging

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


# TODO: correct the response_model
@app.post('/nearest_hospital')  # , response_model=models.Hospital)
async def find_nearest_hospitals(long=None, lat=None):
    """ Receives a position (long, lat) to find the nearest hospitals and
    returns the closest one """
    # MongoDB optimization to have a maximum limit on results
    # As there are currently round abount 2800 hospitals we are safe with this
    # limit as long as we stay in Germany
    limit = 5000
    # The currently shortest calculated distance
    shortest_distance = None
    shorest_hospital = None

    # Get all Hospitals from MongoDB
    hospitals_collection = db.get_database().get_collection('hospitals')
    if not hospitals_collection:
        raise HTTPException(404, detail='No hospitals collection found')

    hospitals = await hospitals_collection.find().to_list(limit)
    # Iterate over all hospitals
    for h in hospitals:
        # Calc distance two the startpoint
        cur_d = calc_line_distance(
            float(long), float(lat),
            float(h['location']['coordinates'][0]),
            float(h['location']['coordinates'][1]))
        # Safe if its the current shortest distance
        if not shortest_distance or cur_d < shortest_distance:
            shortest_distance = cur_d
            shorest_hospital = h

    logging.debug(
            f'start_long: {long}, start_lat: {lat}, calc_line_distance: '
            f'{shortest_distance}, hospital: {shorest_hospital}')

    return str(shorest_hospital)


def calc_line_distance(x1, y1, x2, y2):
    """ Simplest math function to calculate the direct air distance between two
    points """
    d = sqrt((x1-x2)**2 + (y1-y2)**2)
    return d


app.add_route("/graphql", graphql_app)
