import declxml
import json
from agent.config import EMPTY_JSON_DATACITE
from agent.standards import append_non_duplicates


def transform_to_datacite(settings, meta):
    # Initialisation
    dc_data = json.loads(json.dumps(EMPTY_JSON_DATACITE))
    json_data = meta['json_data']

    # Contruct from record
    dc_data['name'] = json_data['name']
    dc_data['titles'].append({'title': "Image archive product of SPOT 6 Satellite on {} for orbit {}".format(
        json_data['production_date'][:10],
        json_data['ORBIT_NUMBER'])})
    dc_data['dates'].append({
        'date': '{}/{}'.format(
            json_data['START'][:10],
            json_data['END'][:10]),
        'dateType': 'Collected'})
    dc_data['publicationYear'] = \
        json_data.get('production_date', '').split('-')[0]
    dc_data['subjects'].append({'subject': 'SPOT 6'})
    dc_data['subjects'].append({'subject': 'NOAMI'})
    dc_data['subjects'].append(
        {'subject': 'AstroSat Optical Modular Instrument'})
    append_non_duplicates(
        dc_data['subjects'],
        {'subject': json_data['ORBIT_NUMBER']})
    append_non_duplicates(
        dc_data['subjects'],
        {'subject': json_data['RECEIVING_STATION']})
    append_non_duplicates(
        dc_data['subjects'],
        {'subject': json_data['ARCHIVING_CENTER']})

    dc_data['geoLocations'] = [{
        'geoLocationPolygons': [{
            'polygonPoints': [
                {
                    "pointLatitude": json_data['geoLocations'][0]['LATITUDE'],
                    "pointLongitude": json_data['geoLocations'][0]['LONGITUDE']
                },
                {
                    "pointLatitude": json_data['geoLocations'][1]['LATITUDE'],
                    "pointLongitude": json_data['geoLocations'][1]['LONGITUDE']
                },
                {
                    "pointLatitude": json_data['geoLocations'][2]['LATITUDE'],
                    "pointLongitude": json_data['geoLocations'][2]['LONGITUDE']
                },
                {
                    "pointLatitude": json_data['geoLocations'][3]['LATITUDE'],
                    "pointLongitude": json_data['geoLocations'][3]['LONGITUDE']
                },
                {
                    "pointLatitude": json_data['geoLocations'][0]['LATITUDE'],
                    "pointLongitude": json_data['geoLocations'][0]['LONGITUDE']
                }
            ]
        }]
    }]

    # Defaults should come from settings
    dc_data['creators'] = [{
        'creatorName': 'Airbus Defence and Space SAS',
        'affiliation': 'Airbus Defence and Space SAS, 5 rue des Satellites BP 14 359, 31030 Toulouse cedex 4, France',
    }]
    dc_data['contributors'] = [
        {'contributorType': 'DataCurator',
         'contributorName': "South African National Space Agency",
         'affiliation': "SANSA, PO Box 484, Silverton 0127, Gauteng, South Africa"},
        {'contributorType': 'Distributor',
         'contributorName': "South African Environmental Observation Network, SAEON, PO Box 2600, Pretoria, 0001, South Africa",
         'affiliation': "SAEON, PO Box 2600, Pretoria, 0001, South Africa"}
    ]
    dc_data['publisher'] = 'South African National Space Agency'
    dc_data['resourceType'] = {
        'resourceType': 'XML',
        'resourceTypeGeneral': 'Dataset'
    }
    dc_data['descriptions'].append({
        'descriptionType': 'Abstract',
        'description': u'The SPOT (Système Pour l’Observation de la Terre or System for Earth Observation) satellites are operated by SPOT Image (created in 1982), a subsidiary of EADS Astrium and based in Toulouse, France. The program was initiated by the French space agency, CNES (Centre national détudes spatiales) in the 1970s in collaboration with the Belgium (SSTC) and Swedish (SNSB) science and space agencies.'})
    dc_data['rightsList'] = [
        {
            'rights': 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
            'rightsURI': 'https://creativecommons.org/licenses/by-sa/4.0'
        }
    ]
    print(str(dc_data))
    return dc_data


geo_processor = declxml.dictionary('CORNER', [
    declxml.string('LATITUDE', required=False),
    declxml.string('LONGITUDE', required=False)
])

xml_processor = declxml.dictionary('AST_Archive_Metadata', [
    declxml.string('Dataset_Id/DATASET_NAME', required=False, alias='name'),
    declxml.string('Processing_Lineage/Production/DATASET_PRODUCTION_DATE', alias="production_date"),
    declxml.string('Pass_Description/RDDF_Pass_Description/ORBIT_NUMBER', required=False, alias='ORBIT_NUMBER'),
    declxml.string('Segment_Description/Data_Strip_Identification/RECEIVING_STATION', required=False, alias='RECEIVING_STATION'),
    declxml.string('Segment_Description/Data_Strip_Identification/ARCHIVING_CENTER', required=False, alias='ARCHIVING_CENTER'),
    declxml.string('Dataset_Id', required=False, alias='name'),
    declxml.array(geo_processor, nested='Segment_Description/Data_Acquisition/Programming/Programming_Geo_Area', alias='geoLocations'),
    declxml.string('Segment_Description/Data_Acquisition/UTC_Acquisition_Range/START', alias='START'),
    declxml.string('Segment_Description/Data_Acquisition/UTC_Acquisition_Range/END', alias='END'),
])
