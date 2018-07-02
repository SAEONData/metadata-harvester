# CherryPy testng details
server_port = 8080
server_url = 'http://localhost:{}'.format(server_port)

# Importer details
import_url = 'http://oa.dirisa.org'
import_user = 'admin'
import_password = ''

# Harvest Options
# transport = 'FileSystem'
# standard = 'CBERS'

# Data Options
source_dir = '/home/mike/projects/harvester/data/CBERS'
server_url = 'http://qa.dirisa.org/Institutions/webtide/metadata'

# Upload data
# upload_server_url = 'http://qa.dirisa.org/Institutions/pixley-ka-seme/pixley-ka-seme/metadata'
# upload_user = 'admin'
# upload_password = ''
upload_server_url = 'http://ckan.dirisa.org:9091/Institutions/webtide/sansa1/metadata'
upload_user = ''
upload_password = ''

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
