"""
This script is ment for initial import of the hospital data into this
application's database. To ensure the import steps are reproducable or can
be adjusted.
"""
import json
import logging
import requests

from backend.wirvsvirus import Hospital


def get_data_from_arcgis():
    """ An API provides the hospital data as a JSON output """
    # TODO: Probably better to move this into a config file, but for the first
    #       draft its configurable directly here in the import function
    REST_API = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/"
    FEATURE_LAYER = "services/Krankenhaus_hospital/FeatureServer/0/query?"
    QUERY = "where=1%3D1&outFields=*&outSR=4326&f=json"
    full_api_call = REST_API + FEATURE_LAYER + QUERY

    # Send Request to Open Street Map API
    response = requests.get(full_api_call)

    # Verification of the response to import broken stuff
    if response.status_code != 200:
        logging.error(
            f"Canceled hospital import, because API Repsonse Status "
            f"Code: {response.status_code}. Expected 200")
        return

    # Work in Progress
    respons_json = json.loads(state)
    # json(response)

    logging.debug("Received {}")

    # Bring this into our Data Model




def initial_hospital_import():
    logging.debug("initial_hospital_import was called. Starting import.")

    # TODO: Configure/retrieve DATA Source
    # TODO: If required process data transformations/replacements etc.
    # TODO: safe into configure database target


if __name__ == '__main__':
    initial_hospital_import()
