"""
This importer script is ment for initial import of the hospital data into this
application's database. To ensure the import steps are reproducable for other
developers and the project database can be initially filled.
"""
import asyncio
import csv
import hashlib
import logging
import sys

from wirvsvirus import db

from wirvsvirus.models import HospitalBase
from wirvsvirus.crud import create_item


async def get_data_from_arcgis_file(file) -> list:
    """ Simulates an API call by reading the json from file, for testing and to
    prevent IP Blocks """

    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            # TODO: Quickly hacked, probably better to cmap the fields and
            #       throw them into the constructor via kwargs-dictionary

            # Creating an access id from the global id for idempotence
            mongo_id = hashlib.sha224(
                row["GlobalID"].encode('utf-8')).hexdigest()
            mongo_id = mongo_id[:24]

            hb = HospitalBase(
                _id=mongo_id,
                name=row["name"],
                address=row["address_full"],
                website=row["contact_website"],
                phone_number=row["contact_phone"],

                operator=row["operator"],
                operator_type=row["operator_type"],
                contact_email=row["contact_email"],
                contact_fax=row["contact_fax"],
                addr=row["addr"],
                address_full=row["address_full"],
                address_street=row["address_street"],
                address_housenumber=row["address_housenumber"],
                address_city=row["address_city"],
                address_suburb=row["address_suburb"],
                address_subdistrict=row["address_subdistrict"],
                address_district=row["address_district"],
                address_province=row["address_province"],
                address_state=row["address_state"],
                denomination=row["denomination"],
                religion=row["religion"],
                emergency=row["emergency"],
                rooms=row["rooms"],
                beds=row["beds"],
                capacity=row["capacity"],
                wheelchair=row["wheelchair"],
                wikidata=row["wikidata"],
                wikipedia=row["wikipedia"],
                orig_fid=row["ORIG_FID"],
                globalid=row["GlobalID"]
                # TODO: Geomety added
                # geometry=[
                #              #    x: row['X'],
                #              #    y: row['Y']
                #              # ]
                )
            await create_item("hospitals", hb)


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
    hospitals = get_data_from_arcgis_file()
    # hospitals = get_data_from_arcgis()

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


class SomeModel:
    """Some model."""
    id = "1"
    name = "stefan"


async def test_db():
    print(db.get_database())


if __name__ == '__main__':
    db.connect()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        get_data_from_arcgis_file('data/hospital_openstreetmap_20200317.csv'))
    loop.close()

   # result = pool.apply_async(
   #     get_data_from_arcgis_file, 'clinics.csv', cb)

    # äawait get_data_from_arcgis_file()

    # test_db()
    # init_logger()
    # initial_hospital_import()
