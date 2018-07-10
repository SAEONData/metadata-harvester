import json
import logging
from agent.config import EMPTY_JSON_DATACITE

logger = logging.getLogger(__name__)


def text_processor(meta, data):

    rows = data.split('\n')
    adict = dict()
    for row in rows:
        # print(row)
        row = row.strip()
        if row.startswith('GROUP'):
            continue
        if row.startswith('END'):
            continue
        row_list = row.split('=')
        if len(row_list) != 2:
            print('text_processor {}: cannot process row {}'.format(
                meta['title'], row))
            # TODO
            continue
        key = row_list[0].strip()
        val = row_list[1].strip().strip('"')
        if key in adict:
            print('text_processor {}: dupliate key {}'.format(
                meta['title'], key))
            continue
        adict[key] = val
        # print('"{}": ["value": "XXXXX", "default": "ZZZZZ"],'.format(key))
    # print(adict)
    return adict


def transform_to_datacite(settings, meta):
    # Initialisation
    dc_data = json.loads(json.dumps(EMPTY_JSON_DATACITE))
    json_data = meta['json_data']

    for key in json_data:
        if key == 'DATE_ACQUIRED':
            date_dict = {'date': json_data[key], 'dateType': 'Collected'}
            dc_data['dates'].append(date_dict)
            title = "Landsat 8 Operational Land Imager and Thermal Infrared Sensor Collection 1 Level-1 {}".format(json_data[key])
            title_dict = {'title': title, 'titleType': ''}
            dc_data['titles'].append(title_dict)
        if key == 'FILE_DATE':
            date_dict = {'date': json_data[key], 'dateType': 'Created'}
            dc_data['dates'].append(date_dict)
            dc_data['publicationYear'] = json_data[key][:4]
        elif key == 'CORNER_UL_LAT_PRODUCT':
            if json_data.get('CORNER_UL_LAT_PRODUCT') and \
               json_data.get('CORNER_LL_LAT_PRODUCT') and \
               json_data.get('CORNER_UL_LON_PRODUCT') and \
               json_data.get('CORNER_LL_LON_PRODUCT'):
                dc_data['geoLocations'] = [{
                    'geoLocationBox': '{} {} {} {}'.format(
                        json_data['CORNER_UL_LAT_PRODUCT'],
                        json_data['CORNER_LL_LAT_PRODUCT'],
                        json_data['CORNER_UL_LON_PRODUCT'],
                        json_data['CORNER_LL_LON_PRODUCT'])}]
        elif key == 'LANDSAT_SCENE_ID':
            alt_dict = {
                'alternateIdentifier': json_data[key],
                'dateType': 'Landsat Scene ID'}
            dc_data['alternateIdentifiers'].append(alt_dict)

    # Defaults should come from settings
    dc_data['creators'] = [{
        'creatorName': 'U.S. Geological Survey (USGS)',
        'affiliation': 'U.S. Geological Survey (USGS) Earth Resources Observation and Science (EROS) Center'
    }]

    dc_data['contributors'] = [{
        'contributorName': 'SANSA',
        'affiliation': 'South African National Space Agency~DataCurator~PO Box 484, Silverton 0127, Gauteng, South Africa'
    }, {
        'contributorName': 'SAEON',
        'affiliation': 'South African Environmental Observation Network~Distributor~SAEON, PO Box 2600, Pretoria, 0001, South Africa'
    }]
    dc_data['publisher'] = 'South African National Space Agency'
    dc_data['description'] = [{
        'description': 'The Landsat program, originally known as the Earth Resources Technology Satellite (ERTS), was proposed in 1965 by the US Geological Survey (USGS) as a civilian satellite program. NASA started building the first satellite in 1970 and have launched 6 spacecraft successfully (Landsat 6 was lost at launch). In December 2009 all Landsat archive products were made available free to the public on the USGS website.'
        'Landsat 8 carries the Operational Land Imager (OLI) and the Thermal Infrared Sensor (TIRS) data recorder. The OLI sensor includes two additional bands compared to previous Landsat missions: a coastal aerosol band and a cirrus cloud band. The TIRS sensor provides data in two bands with different wavelengths and is resampled to 30m from 100m acquisition resolution. All products are provided in the 16-bit data range and have improved radiometric and geometric performance. Landsat 8 is offset from the Landsat 7 orbit by 8 days giving a shorter revisit time between the two satellites.',
        'descriptionType': 'Abstract'}]
    dc_data['resourceType'] = 'Satellite Data'
    dc_data['resourceTypeGeneral'] = 'Dataset'
    dc_data['subjects'].append({'subject': 'Sensor Type: Optical'})
    dc_data['subjects'].append({'subject': 'Reference System: Worldwide Reference System 2 (WRS2)'})
    dc_data['subjects'].append({'subject': 'Scanner Type: Push Broom Optical Scanner'})
    dc_data['subjects'].append({'subject': 'Swath: 185 km'})
    dc_data['subjects'].append({'subject': 'Bands: 11'})
    dc_data['subjects'].append({'subject': 'Band Type: Multi-spectral, Panchromatic, Thermal'})
    dc_data['subjects'].append({'subject': 'Spectral Range: 430 - 12510 nm'})
    dc_data['subjects'].append({'subject': 'Spatial Resolution: 15m, 30m'})
    dc_data['subjects'].append({'subject': 'Quantization: 12'})
    dc_data['subjects'].append({'subject': 'Image Size: 185 km x 170 km'})
    dc_data['subjects'].append({'subject': 'Landsat 8'})
    dc_data['subjects'].append({'subject': 'OLI'})
    dc_data['subjects'].append({'subject': 'pan-sharpen'})
    dc_data['subjects'].append({'subject': 'TIRS'})
    dc_data['subjects'].append({'subject': '30m resampled'})
    dc_data['subjects'].append({'subject': '100m acquired'})
    dc_data['rights'] = [{
        'rights': 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
        'rightsURI': 'https://creativecommons.org/licenses/by-sa/4.0/'}]
    dc_data['language'] = 'en-us'
    dc_data['version'] = '3.1'
    dc_data['xsiSchema'] = [
        'http://datacite.org/schema/kernel-3 '
        'http://schema.datacite.org/meta/kernel-3/metadata.xsd']
    return dc_data
