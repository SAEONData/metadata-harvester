# Harvest XML metadata files and upload them into a SAEON CKAN metadata server

## Deployment

### System dependencies
* python3 (&ge; 3.5)
* requests
* cherrypy

### Package installation
Assuming the Agent repository has been cloned to `$AGENTDIR`, install the Agent
and its remaining package dependencies with:

    pip3 install $AGENTDIR


## Usage

### JSON API
#### harvest
Harvest XML metadata files and upload them into a SAEON CKAN metadata server

##### Arguments:
* transport: transport protocol to gather data. Currently only supports "FileSystem".
* source_dir: the directory on the local file system where the text files reside
* standard: the metadta type of the data files
* upload_server_url: the end point into which the harvested records will be uploaded using either the give upload_method or jsonCreateMetadataAsJson
* upload_user: the user to be used to add new records at the given upload_server_url
* upload_password: the password to be used to add new records at the given upload_server_url
* upload_method: the method to be used to add new records at the given upload_server_url


## Unit Tests

python agent/tests/test_unit_transform.py

