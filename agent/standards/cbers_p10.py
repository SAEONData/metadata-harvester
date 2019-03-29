import declxml
import json
from agent.config import EMPTY_JSON_DATACITE


def transform_to_datacite(settings, meta):
    # Initialisatio Hack
    dc_data = json.loads(json.dumps(EMPTY_JSON_DATACITE))
    json_data = meta['json_data']

    # Contruct from record
    dc_data['name'] = json_data['sceneId']
    dc_data['titles'].append({'title': '{} {} for {} {} {}'.format(
        json_data['satelliteId'],
        json_data['sensorId'],
        json_data['productType'],
        json_data['productId'],
        json_data['productLevel']
    )})
    dc_data['dates'].append({
        'date':
            '{}/{}'.format(
                json_data['imagingStartTime'][:10],
                json_data['imagingStopTime'][:10]),
        'dateType': 'Collected'})
    dc_data['publicationYear'] = \
        json_data.get('productDate', '').split('-')[0]
    dc_data['subjects'].append({'subject': json_data['dataFormatDes']})
    dc_data['subjects'].append({'subject': json_data['earthModel']})
    dc_data['subjects'].append({'subject': json_data['mapProjection']})
    dc_data['subjects'].append({'subject': json_data['satelliteId']})
    dc_data['subjects'].append({'subject': json_data['sensorId']})
    dc_data['subjects'].append({'subject': json_data['productLevel']})

    dc_data['geoLocations'] = [{
        'geoLocationPolygons': [{
            'polygonPoints': [
                {
                    "pointLatitude": json_data['dataUpperLeftLat'],
                    "pointLongitude": json_data['dataUpperLeftLong']
                },
                {
                    "pointLatitude": json_data['dataLowerLeftLat'],
                    "pointLongitude": json_data['dataLowerLeftLong']
                },
                {
                    "pointLatitude": json_data['dataLowerRightLat'],
                    "pointLongitude": json_data['dataLowerRightLong']
                },
                {
                    "pointLatitude": json_data['dataUpperRightLat'],
                    "pointLongitude": json_data['dataUpperRightLong']
                },
                {
                    "pointLatitude": json_data['dataUpperLeftLat'],
                    "pointLongitude": json_data['dataUpperLeftLong']
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
        'description': "The China–Brazil Earth Resources Satellite program (CBERS) is a technological cooperation program between Brazil and China. CBERS satellites has a number of different sensors depending on the satellite. This is the CBERS({satelliteId}) collecting in {instrumentMode} with the sensor {sensorId} with a {productType} product type at a {productLevel} processing level.".format(**json_data)})
    dc_data['rightsList'] = [
        {
            'rights': 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
            'rightsURI': 'https://creativecommons.org/licenses/by-sa/4.0'
        }
    ]
    dc_data['subjects'].append({'subject': 'P10 Sensor Type'})
    dc_data['subjects'].append({'subject': 'WGS84 Reference System'})
    dc_data['subjects'].append({'subject': 'Single Banded'})
    return dc_data


xml_processor = declxml.dictionary('root/data', [
    declxml.string('productId', required=True),
    declxml.string('productType', required=True),
    declxml.string('productLevel', required=True),
    declxml.string('productDate', required=True),
    declxml.string('sceneId', required=True),
    declxml.string('satelliteId', required=True),
    declxml.string('sensorId', required=True),
    declxml.string('imagingStartTime', required=True),
    declxml.string('imagingStopTime', required=True),
    declxml.string('dataFormatDes', required=True),
    declxml.string('earthModel', required=True),
    declxml.string('mapProjection', required=True),
    declxml.string('dataLowerLeftLat', required=True),
    declxml.string('dataLowerLeftLong', required=True),
    declxml.string('dataUpperRightLat', required=True),
    declxml.string('dataUpperRightLong', required=True),

    declxml.string('recStationId', required=False),
    declxml.string('pixelSpacing', required=False),
    declxml.string('sceneCount', required=False),
    declxml.string('sceneShift', required=False),
    declxml.string('overallQuality', required=False),
    declxml.string('satPath', required=False),
    declxml.string('satRow', required=False),
    declxml.string('satPathbias', required=False),
    declxml.string('satRowbias', required=False),
    declxml.string('scenePath', required=False),
    declxml.string('sceneRow', required=False),
    declxml.string('scenePathbias', required=False),
    declxml.string('sceneRowbias', required=False),
    declxml.string('direction', required=False),
    declxml.string('sunElevation', required=False),
    declxml.string('sunAzimuthElevation', required=False),
    declxml.string('sceneDate', required=False),
    declxml.string('sceneTime', required=False),
    declxml.string('instrumentMode', required=False),
    declxml.string('gain', required=False),
    declxml.string('satOffNadir', required=False),
    declxml.string('mirrorOffNadir', required=False),
    declxml.string('bands', required=False),
    declxml.string('absCalibType', required=False),
    declxml.string('mtfcProMode', required=False),
    declxml.string('radioMatricMethod', required=False),
    declxml.string('addWindow', required=False),
    declxml.string('correctPhase', required=False),
    declxml.string('reconstructProcess', required=False),
    declxml.string('resampleTechnique', required=False),
    declxml.string('productOrientation', required=False),
    declxml.string('ephemerisData', required=False),
    declxml.string('attitudeData', required=False),
    declxml.string('sceneCenterLat', required=False),
    declxml.string('sceneCenterLong', required=False),
    declxml.string('zone', required=False),
    declxml.string('dataUpperLeftLat', required=False),
    declxml.string('dataUpperLeftLong', required=False),
    declxml.string('dataLowerRightLat', required=False),
    declxml.string('dataLowerRightLong', required=False),
    declxml.string('productUpperLeftLat', required=False),
    declxml.string('productUpperLeftLong', required=False),
    declxml.string('productUpperRightLat', required=False),
    declxml.string('productUpperRightLong', required=False),
    declxml.string('productLowerLeftLat', required=False),
    declxml.string('productLowerLeftLat', required=False),
    declxml.string('productLowerRightLat', required=False),
    declxml.string('productLowerRightLong', required=False),
    declxml.string('dataUpperLeftX', required=False),
    declxml.string('dataUpperLeftY', required=False),
    declxml.string('dataUpperRightX', required=False),
    declxml.string('dataUpperRightY', required=False),
    declxml.string('dataLowerLeftX', required=False),
    declxml.string('dataLowerLeftY', required=False),
    declxml.string('dataLowerRightX', required=False),
    declxml.string('dataLowerRightY', required=False),
    declxml.string('productUpperLeftX', required=False),
    declxml.string('productUpperLeftY', required=False),
    declxml.string('productUpperRightX', required=False),
    declxml.string('productUpperRightY', required=False),
    declxml.string('productLowerLeftX', required=False),
    declxml.string('productLowerLeftY', required=False),
    declxml.string('productLowerRightX', required=False),
    declxml.string('productLowerRightY', required=False),
    declxml.string('isSimulateData', required=False),
    declxml.string('delStatus', required=False),
    declxml.string('dataTempDir', required=False),
    declxml.string('dataArchiveDir', required=False),
    declxml.string('browseArchiveDir', required=False),
    declxml.string('browseDirectory', required=False),
    declxml.string('browseFileLocation', required=False),
])
