"""Setup an API."""

from typing import List, Any
from datetime import datetime, timedelta
from uuid import UUID
from math import sqrt
import logging

from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from bson import ObjectId

from wirvsvirus import db, models, auth, crud
from wirvsvirus.graphql_ariadne import graphql_app
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
async def post_profile(profile: models.ProfileInput, db: db.AsyncIOMotorDatabase = Depends(db.get_database), jwt_payload: dict = Depends(auth.auth)):
    """Create your profile.

    This creates the currently authenticated users profile.
    After authenticating, we need to first create this profile before further actions can be taken.

    Note that the fields "helper" and "hospital_id" must be filled depending on
    the setting of "profileType":

    * If profileType is set to "helper", the "helper" object MUST be also
      supplied. This object will be used to create a "helper" object.
    * If profileType is set to "hospital", the "hospitalId" field MUST be
      supplied and the corresponding hospital must exist.

    WARNING: Once a profile is created it cannot be changed.

    """
    intermediate_profile = models.ProfileIntermediate(**profile.dict(), user_id=jwt_payload['sub'])
    db_profile = await db.profiles.find_one({'user_id': intermediate_profile.user_id})
    if db_profile:
        raise HTTPException(409, detail='profile already exists!')

    if profile.profile_type == models.ProfileTypeEnum.helper:
        if not profile.helper:
            raise HTTPException(400, "Missing helper definition for helper user profile.")
        document = await crud.create_item('helpers', profile.helper)
        helper = models.Helper(**document)
        intermediate_profile.helper_id = helper.id
        intermediate_profile.hospital_id = None
    elif profile.profile_type == models.ProfileTypeEnum.hospital:
        if not profile.hospital_id:
            raise HTTPException(400, "Missing hospital id for hospital user profile.")
        document = await crud.get_item('hospitals', ObjectId(intermediate_profile.hospital_id))
        if not document:
            raise HTTPException(404, 'Given hospital_id does not exist.')
        intermediate_profile.helper_id = None
    else:
        raise NotImplementedError('profile type not implemented')

    # When everything else is done, finally create the profile
    return await crud.create_item('profiles', intermediate_profile)

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


@app.get('/matches/propositions', response_model=models.MatchProposition)
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
    return {"allocations": model.results["allocations"]}


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
async def find_nearest_hospitals(lon=None, lat=None):
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
            float(lon), float(lat),
            float(h['location']['coordinates'][0]),
            float(h['location']['coordinates'][1]))
        # Safe if its the current shortest distance
        if not shortest_distance or cur_d < shortest_distance:
            shortest_distance = cur_d
            shorest_hospital = h

    logging.debug(
            f'start_long: {lon}, start_lat: {lat}, calc_line_distance: '
            f'{shortest_distance}, hospital: {shorest_hospital}')

    return str(shorest_hospital)


def calc_line_distance(x1, y1, x2, y2):
    """ Simplest math function to calculate the direct air distance between two
    points """
    d = sqrt((x1-x2)**2 + (y1-y2)**2)
    return d


app.add_route("/graphql", graphql_app)
