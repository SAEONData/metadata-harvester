# CherryPy testng details
server_port = 8080
server_url = 'http://localhost:{}'.format(server_port)

# Importer details
import_url = 'http://oa.dirisa.org'
import_user = 'admin'
import_password = ''

# Harvest Options
transport = 'FileSystem'
standard = 'CBERS'

# Data Options
source_dir = '/home/mike/projects/harvester/data/CBERS'
# server_url = 'http://qa.dirisa.org/Institutions/pixley-ka-seme/pixley-ka-seme/metadata'

# Upload data
upload_server_url = 'http://ckan.dirisa.org:9090/Institutions/webtide1/sansa3/metadata'
upload_user = ''
upload_password = ''
metadata_dict = {
    'titles': [],
    'alternateIdentifiers': [],
    'creators': [{
        'creatorName': 'U.S. Geological Survey (USGS) Earth Resources Observation and Science (EROS) Center'
    }],
    'contributors': [{
        'contributorName': 'South African National Space Agency~DataCurator~PO Box 484, Silverton 0127, Gauteng, South Africa'
    }, {
        'contributorName': 'South African Environmental Observation Network~Distributor~SAEON, PO Box 2600, Pretoria, 0001, South Africa'
    }],
    'dates': [],
    'publisher': 'South African National Space Agency',
    'description': [{
        'description': 'The Landsat program, originally known as the Earth Resources Technology Satellite (ERTS), was proposed in 1965 by the US Geological Survey (USGS) as a civilian satellite program. NASA started building the first satellite in 1970 and have launched 6 spacecraft successfully (Landsat 6 was lost at launch). In December 2009 all Landsat archive products were made available free to the public on the USGS website.'

        'Landsat 8 carries the Operational Land Imager (OLI) and the Thermal Infrared Sensor (TIRS) data recorder. The OLI sensor includes two additional bands compared to previous Landsat missions: a coastal aerosol band and a cirrus cloud band. The TIRS sensor provides data in two bands with different wavelengths and is resampled to 30m from 100m acquisition resolution. All products are provided in the 16-bit data range and have improved radiometric and geometric performance. Landsat 8 is offset from the Landsat 7 orbit by 8 days giving a shorter revisit time between the two satellites.',
        'descriptionType': 'Abstract'}],
    'resourceType': 'Satellite Data',
    'resourceTypeGeneral': 'Dataset',
    'subjects': [
        {'subject': 'Sensor Type: Optical'},
        {'subject': 'Reference System: Worldwide Reference System 2 (WRS2)'},
        {'subject': 'Scanner Type: Push Broom Optical Scanner'},
        {'subject': 'Swath: 185 km'},
        {'subject': 'Bands: 11'},
        {'subject': 'Band Type: Multi-spectral, Panchromatic, Thermal'},
        {'subject': 'Spectral Range: 430 - 12510 nm'},
        {'subject': 'Spatial Resolution: 15m, 30m'},
        {'subject': 'Quantization: 12'},
        {'subject': 'Image Size: 185 km x 170 km'},
        {'subject': 'Landsat 8'},
        {'subject': 'OLI'},
        {'subject': 'pan-sharpen'},
        {'subject': 'TIRS'},
        {'subject': '30m resampled'},
        {'subject': '100m acquired'},
    ],
    'rights': [{
        'rights': 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
        'rightsURI': 'https://creativecommons.org/licenses/by-sa/4.0/'}],
    'language': 'en-us',
    'version': '3.1',
    'xsiSchema': 'http://datacite.org/schema/kernel-3 '
                 'http://schema.datacite.org/meta/kernel-3/metadata.xsd',
}

metadata_dict_example = {
    'additionalFields': {
        'coverageBegin': '',
        'coverageEnd': '',
        'onlineResources': [
            {'desc': 'Original Metadata Record',
             'func': 'metadata',
             'href': 'http://qa.dirisa.org/Portals/test-mike/testcustmike/metadata/metadata.2018-02-28.9981326861/getOriginalXml',
             'name': 'Original Metadata Record'}],
        'source_uri': '',
        'status': 'complete'
    },
    'alternateIdentifiers': [{
        'alternateIdentifier': 'http://schema.datacite.org/schema/meta/kernel-3.1/example/datacite-example-full-v3.1.xml',
        'alternateIdentifierType': 'URL'}],
    'bounds': [-68.302, 30.233, -66.302, 32.233000000000004],
    'contributors': [{
        'affiliation': 'California Digital Library',
        'contributorName': 'Starr, Joan',
        'contributorType': 'ProjectLeader',
        'nameIdentifier': '0000-0002-7285-027X',
        'nameIdentifierScheme': 'ORCID',
        'schemeURI': 'http://orcid.org/'}],
    'creators': [{
        'affiliation': 'DataCite',
        'creatorName': 'Miller, Elizabeth',
        'nameIdentifier': '0000-0001-5000-0007',
        'nameIdentifierScheme': 'ORCID',
        'schemeURI': 'http://orcid.org/'}],
    'dates': [{'date': '2015-01-01/2019-12-31',
               'dateType': 'Submitted'}],
    'description': [{
        'description': 'XML example of all DataCite '
                       'Metadata Schema v3.1 properties.',
        'descriptionType': 'Abstract'}],
    'errors': [],
    'formats': ['application/xml'],
    'geoLocations': [{
        'geoLocationBox': '41.090 -71.032  42.893 -68.211',
        'geoLocationPlace': 'Atlantic Ocean',
        'geoLocationPoint': '31.233 -67.302'}],
    'identifier': {
        'identifier': '10.5072/example-full', 'identifierType': 'DOI'},
    'language': 'en-us',
    'publicationYear': '2014',
    'publisher': 'DataCite',
    'relatedIdentifiers': [{
        'relatedIdentifier': 'http://data.datacite.org/application/citeproc+json/10.5072/example-full',
        'relatedIdentifierType': 'URL',
        'relatedMetadataScheme': 'citeproc+json',
        'relatedType': 'IsMetadataFor',
        'relationType': 'HasMetadata',
        'schemeType': '',
        'schemeURI': 'https://github.com/citation-style-language/schema/raw/master/csl-data.json'},
        {
        'relatedIdentifier': 'arXiv:0706.0001',
        'relatedIdentifierType': 'arXiv',
        'relatedMetadataScheme': '',
        'relatedType': 'IsMetadataFor',
        'relationType': 'IsReviewedBy',
        'schemeType': '',
        'schemeURI': ''}],
    'resourceType': 'XML',
    'resourceTypeGeneral': 'Software',
    'rights': [{
        'rights': 'CC0 1.0 Universal',
        'rightsURI': 'http://creativecommons.org/publicdomain/zero/1.0/'}],
    'schemaSpecific': {},
    'sizes': ['3KB', '25ml'],
    'subjects': [{
        'schemeURI': 'http://dewey.info/',
        'subject': 'computer science',
        'subjectScheme': 'dewey'}],
    'subtitle': '',
    'title': 'Full DataCite XML Example',
    'titles': [
        {'title': 'Full DataCite XML Example', 'titleType': ''},
        {'title': 'Demonstration of DataCite Properties.',
         'titleType': 'Subtitle'}],
    'version': '3.1',
    'xsiSchema': 'http://datacite.org/schema/kernel-3 '
                 'http://schema.datacite.org/meta/kernel-3/metadata.xsd'
}
