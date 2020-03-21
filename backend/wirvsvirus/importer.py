"""
This importer script is ment for initial import of the hospital data into this
application's database. To ensure the import steps are reproducable for other
developers and the project database can be initially filled.
"""
import json
import logging
import requests
import sys

from settings import settings


def get_data_from_arcgis() -> list:
    """ An API which provides the hospital data as a JSON output """
    # TODO: Probably better to move this into a config file, but for the first
    #       draft its configurable directly here in the import function
    REST_API = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/"
    FEATURE_LAYER = "services/Krankenhaus_hospital/FeatureServer/0/query?"
    QUERY = "where=1%3D1&outFields=*&outSR=4326&f=json"
    full_api_call = REST_API + FEATURE_LAYER + QUERY

    # Variables to manage the request loop
    exceeded_transfer_limit = None
    cur_result_offset = 0
    hospitals = []

    # Repeat the query loop until we received all results
    while exceeded_transfer_limit is None or exceeded_transfer_limit:
        # build the new offset parameter position
        offset_url_param = f'&resultOffset={cur_result_offset}'

        # Send Request to Open Street Map API
        response = requests.get(full_api_call + offset_url_param)

        # Verification of the response to import broken stuff
        if response.status_code != 200:
            logging.critical(
                f"Canceled hospital import, because API Repsonse Status "
                f"Code: {response.status_code}. Expected 200")
            return None

        # Work in Progress
        json_data = json.loads(response.text)
        # json(response)

        # logging.debug(json_data)
        logging.debug(f"Received {len(json_data['features'])} feature objects")
        # Adding the received hospitals into the result list in raw format
        hospitals += json_data['features']

        # Calculating the new offset position based on the received objects
        cur_result_offset += len(json_data['features'])

        if 'exceededTransferLimit' in json_data:
            exceeded_transfer_limit = json_data['exceededTransferLimit']
        else:
            exceeded_transfer_limit = False
    return hospitals


def get_data_from_arcgis_file(file) -> list:
    """ Simulates an API call by reading the json from file, for testing and to
    prevent IP Blocks """
    pass


def transform_arcgis_data(hospitals):
    """ Transforms the received data from the API to fit better into our needs.
    Receives a list with hospital-dictionaries with RAW data from the arcgis
    API and returns also a list with hospital-dictionaries, but little bit
    more adjusted.
    """
    result = []

    for hospital in hospitals:
        new_hospital = {}
        # Move geo coordinates into the hospital attributes
        hospital['attributes']['geometry'] = hospital['geometry']

        # Replace the "underscore" separator for address parts into
        # a dictionary addr_city -> addr: {city: '...'}
        print(hospital['attributes'])
        new_hospital.update(hospital['attributes'])

        # TODO: also replace GLOBALID -> _id

    result.append(new_hospital)
    return result


def initial_hospital_import():
    logging.debug("initial_hospital_import was called. Starting import.")
    # TODO: Configure/retrieve DATA Source
    hospitals = get_data_from_arcgis()

    # Transform the received data a little bit to fit better our purposes
    # TODO: Currently only one result is transformed, needs to be fixed - wip
    # hospitals = transform_arcgis_data(hospitals)

    for h in hospitals:
        if h['address_city']:
            print(f" ----------> '{h['name']}' in "
                  f" {h['address_city']}")
    # TODO: If required process data transformations/replacements etc.
    # TODO: safe into configure database target


def init_logger():
    # TODO: discuss with the team if there is a better place for this config
    loglevel = logging.DEBUG
    logging.basicConfig(
        stream=sys.stderr, level=loglevel,
        format='%(asctime)s [%(levelname)s] %(name)s %(message)s')


if __name__ == '__main__':
    print(settings)
    init_logger()
    initial_hospital_import()
