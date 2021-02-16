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
