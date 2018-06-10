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
# upload_server_url = 'http://ckan.dirisa.org:9090/Institutions/webtide1/sansa3/metadata'
upload_server_url = 'http://qa.dirisa.org/Institutions/pixley-ka-seme/pixley-ka-seme/metadata'
upload_user = 'admin'
upload_password = 'editbew123'

EMPTY_JSON_DATACITE = {
    "titles": [],
    "subtitle": "",
    "contributors": [],
    "userId": "",
    "xsiSchema": "http://datacite.org/schema/kernel-3",
    "owner": "",
    "subjects": [],
    "geoLocations": [],
    "userVersion": "",
    "description": [],
    "publicationYear": "",
    "relatedIdentifiers": [],
    "creators": [],
    "publisher": "",
    "dates": [],
    "language": "eng",
    "rights": [],
    "resourceType": "",
    "sizes": [],
    "resourceTypeGeneral": "",
    "bounds": [],
    "alternateIdentifiers": [],
    "identifier": {},
    "additionalFields": {
        'onlineResources': ''
    },
}
