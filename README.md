# Metadata Search Agent using Elastic Search

## Deployment

### System dependencies
* python3 (&ge; 3.6)
* requests
* cherrypy

### Package installation
Assuming the Agent repository has been cloned to `$AGENTDIR`, install the Agent
and its remaining package dependencies with:

    pip3 install $AGENTDIR


## Usage

### JSON API
#### search
Return selected records in a 'SAEON JSON DataCite' format
##### Arguments:
* field/value pairs: provide any number of fields with the search value
