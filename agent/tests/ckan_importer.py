#!/usr/bin/python3

import argparse
from datetime import datetime
import json
import logging
import requests
import time
import re
import sys

import_to_ckan = True
import_to_agent = False

# Constants
# Source config
# src_base_url = 'http://qa.dirisa.org'
src_base_url = 'http://oa.dirisa.org'
#src_base_url = 'http://oa.dirisa.org/Institutions/carbon-atlas/carbon-atlas'
# src_base_url = 'http://localhost:8080/SAEON'

# ES destination config
agent_base_url = 'http://localhost:9210'
agent_user = 'admin'
metadata_index_name = 'md_index_1'

# CKAN destination config
ckan_base_url = 'http://192.168.111.56:8979'#'http://ckan.dirisa.org:9090'
ckan_user = 'mike@webtide.co.za'


UPDATE_METRICS = {
    'update_count':0,
    'records_added':0,
    'validated_successfully':0,
    'validation_errors': 0,
    'published':0,
    'unpublished':0,
}

def gen_unique_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def get_physical_path(url):
    idx = 3
    if 'localhost' in url:
        idx = 4
    return '/'.join(url.split('/')[idx:])

def set_workflow_state(state, record_id, organization, val_result):
    #print("Setting state for uid{}".format(record_id))
    data = {
        #'recordId': record_id,
        'state': state
    }
    org_id_reformatted = re.sub(r'[^a-z0-9_-]+', '-', organization['title'].lower())
    #url = "{}/setWorkflowState".format(
    #    ckan_base_url, org_id_reformatted, org_id_reformatted)
    url = "{}/metadata/workflow/{}".format(
        ckan_base_url, record_id)
    #print(data)
    #print(url)
    response = requests.post(
        url=url,
        params=data,
        #auth=requests.auth.HTTPBasicAuth(
        #    creds['ckan_user'], creds['ckan_pwd'])
    )

    result = None
    try:
        result = json.loads(response.text)
    except Exception:
        logging.error("Couldn't decode resoponse {} {}".format(response.status_code, response.text))
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))

    print("set workflow state result {}".format(result))
    state_unchanged = False
    if response.status_code != 200 and ('message' not in result['detail']):
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))
    if response.status_code != 200 and ('message' in result['detail']) and \
        (result['detail']['message'] != \
            'The metadata record is already assigned the specified workflow state'):
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))
    elif response.status_code != 200 and ('message' in result['detail']) and \
        (result['detail']['message'] == \
            'The metadata record is already assigned the specified workflow state'):
        logging.info('The metadata record is already assigned the specified workflow state {}'.format(state))
        state_unchanged = True

    #print("## workflow status update result ###")

    #if 'detail' in 

    if not state_unchanged and result['success']:#
        msg = 'Workflow status updated to {}'.format(state)
        logging.info(msg)
        return True
    else:
        #show_error = True
        #if ('message' in result['msg']) and \
        #    (result['msg']['message'].__contains__(
        #        'The metadata record is already assigned the specified workflow state')):
        #        msg = "Already assigned state {}".format(state)
        #        logging.info(msg)
        #        show_error = False
        if not state_unchanged:
            msg = 'Workflow status could not be updated!\n Error {}'.format(result)
            logging.error(msg)
            #logging.error(val_result)
            #print(val_result)
            return False

def add_a_record_to_ckan(collection, metadata_json, organization, record_id, infrastructures, state):

    #data = {
    #    'jsonData': json.dumps(metadata_json),
    #    'metadataType': 'datacite-4-2',
    #    'targetWorkflowState': 'plone-published',
    #    'fallbackWorkflowState': 'plone-provisional' 
    #}

    org_id_reformatted = re.sub(r'[^a-z0-9_-]+', '-', organization['title'].lower())
    #url = "{}/Institutions/{}/{}-repository/metadata/jsonCreateMetadataAsJson".format(
    #    ckan_base_url, org_id_reformatted, org_id_reformatted)

    url = "{}/metadata/".format(ckan_base_url)

    print("trying to add record into {}".format(org_id_reformatted))
    print(org_id_reformatted + '-metadata')
    record_data = {
            "institution": org_id_reformatted,
            "metadata_standard": 'saeon-odp-4-2',
            "metadata": metadata_json,#json.dumps(metadata_json),
            "infrastructures": [],
            "collection": org_id_reformatted + '-metadata'
    }

    response = requests.post(
        url=url,
        json=record_data
        #params=data,
        #auth=requests.auth.HTTPBasicAuth(
        #    creds['ckan_user'], creds['ckan_pwd'])
    )
    #print(url)
    #response = requests.post(
    #    url=url,
    #    params=data,
    #    auth=requests.auth.HTTPBasicAuth(
    #        creds['ckan_user'], creds['ckan_pwd'])
    #)
    print("add record response {}".format(response.text))
    if response.status_code != 200:
        #if check_record_empty(record_data['metadata']):
        #    print("Record is empty!!!")
        #else:
        #    print(url)
        #    record_data['metadata'].pop('original_xml')
        #    record_data['metadata'].pop('errors')
        #    print(record_data['metadata'])

        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))
    result = json.loads(response.text)
    print("#### RESULT ####")

    print(result.keys())
    #if result['status'] == 'success':

    if check_ckan_added(organization, result):
        msg = 'Added Successfully'
        logging.info(msg)

        UPDATE_METRICS['records_added'] = UPDATE_METRICS['records_added'] + 1

    else:
        msg = 'Record not found'
        logging.info(msg)
    #if result['workflow_status'] == 'failed':
    #    print('But workflow failed: {}'.format(result['workflow_msg']))
    record_id = result['id']

    if result['validated'] and (len(result['errors'].keys()) == 0):#result['validate_status'] == 'success':
        msg = "Validated successfully, advancing state"
        logging.info(msg)
        updated = set_workflow_state('plone-published', record_id, organization, result)
        UPDATE_METRICS['validated_successfully'] = UPDATE_METRICS['validated_successfully'] + 1
        if updated:
            UPDATE_METRICS['published'] = UPDATE_METRICS['published'] + 1

    elif result['validated'] and (len(result['errors'].keys()) > 0):
        msg = "Validation errors:\n {}\nAttempting published state".format(result['errors'])
        logging.error(msg)
        #logging.error(result)
        updated = set_workflow_state('plone-published', record_id, organization, result)
        if updated:
            msg = "Successfully published with validation errors"
            logging.error(msg)
            UPDATE_METRICS['validated_successfully'] = UPDATE_METRICS['validated_successfully'] + 1
            UPDATE_METRICS['published'] = UPDATE_METRICS['published'] + 1
        else:
        #print(metadata_json)
            msg = "Unable to publish with validation errors, setting state to provisional"
            logging.error(msg)
            logging.error(result)
            updated = set_workflow_state('plone-provisional', record_id, organization, result)
            UPDATE_METRICS['validation_errors'] = UPDATE_METRICS['validation_errors'] + 1
            if updated:
                UPDATE_METRICS['unpublished'] = UPDATE_METRICS['unpublished'] + 1

    else:
        msg = 'Request to add record failed'
        logging.error(msg)
        logging.error(result)
    #    #print(result)
    return result


def add_a_record_to_elastic(collection, metadata_json, organization, record_id, infrastructures):

    data = {
        'metadata_json': json.dumps(metadata_json),
        'index': metadata_index_name,
        'collection': collection,
        'infrastructures': infrastructures,
        'organization': organization['title'],
        'record_id': record_id,
    }
    url = "{}/add".format(agent_base_url)
    response = requests.post(
        url=url,
        params=data,
        auth=requests.auth.HTTPBasicAuth(
            creds['agent_user'], creds['agent_pwd'])
    )
    if response.status_code != 200:
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))
    result = json.loads(response.text)
    if result['success']:
        if import_to_agent:
            if check_agent_added(organization, record_id):
                print('Added Successfully')
            else:
                print('Record not found')
    else:
        print(result)
    return result


def check_ckan_added(organization, result):
    time.sleep(1)
    # Find the record via jsonContent
    record_id = result['id']
    #data = {
    #    'types': 'Metadata',
    #}
    org_id_reformatted = re.sub(r'[^a-z0-9_-]+', '-', organization['title'].lower())
    #url = "{}/Institutions/{}/{}-repository/metadata/jsonContent".format(
    #    ckan_base_url, org_id_reformatted, org_id_reformatted)
    url = "{}/metadata/{}".format(
        ckan_base_url, record_id)
    try:
        response = requests.get(
            url=url,
            #params=data,
            #auth=requests.auth.HTTPBasicAuth(
            #    creds['ckan_user'], creds['ckan_pwd'])
        )
    except Exception as e:
        print(e)
        return False

    if response.status_code != 200:
        # raise RuntimeError('Request failed with return code: %s' % (
        #     response.status_code))
        return False

    found = False
    result = json.loads(response.text)
    #print("checking result {}".format(result))

    if result['id'] == record_id:
        found = True
    return found


def check_agent_added(organization, record_id):

    time.sleep(1)
    data = {
        'record_id': record_id,
        'index': metadata_index_name,
    }
    url = "{}/search".format(agent_base_url)
    response = requests.get(
        url=url,
        params=data,
        auth=requests.auth.HTTPBasicAuth(
            creds['agent_user'], creds['agent_pwd'])
    )
    if response.status_code != 200:
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))
    # print(response.text)
    result = json.loads(response.text)
    if not result['success']:
        raise RuntimeError('Request failed with response: %s' % (
            result.get('msg', 'Dunno')))
    if result['result_length'] == 0:
        print(record_id)
        return False

    return True


def download_xml(url, creds):
    url = "{}/getOriginalXml".format(url)
    #print(url)
    response = requests.get(
        url=url,
        auth=requests.auth.HTTPBasicAuth(
            creds['src_user'], creds['src_pwd'])
    )
    if response.status_code != 200:
        return 'Request failed with return code: %s' % (
            response.status_code)

    return response.text


def get_metadata_records(path, creds):

    url = "{}/{}/jsonGetRecords".format(src_base_url, path)
    response = requests.get(
        url=url,
        auth=requests.auth.HTTPBasicAuth(
            creds['src_user'], creds['src_pwd'])
    )
    if response.status_code != 200:
        return 'Request failed with return code: %s' % (
            response.status_code)

    return response.text


def get_institutions(creds, institutions_list):

    url = "{}/Institutions/jsonContent?types=Institution".format(src_base_url)
    try:
        response = requests.get(
            url=url,
            auth=requests.auth.HTTPBasicAuth(
                creds['src_user'], creds['src_pwd'])
        )
    except Exception as e:
        print(e)
        return str(e)

    if response.status_code != 200:
        return 'Request failed with return code: %s' % (
            response.status_code)

    results = json.loads(response.text)
    institutions = []
    for result in results:
        inst = {
            'id': result['id'],
            'title': result['title'],
            'path': get_physical_path(result['context_path'])
        }
        institutions.append(inst)

    # remove institutions not in list, if it exists
    rem_count = 0
    if institutions_list:
        for i in range(len(institutions)):
            if institutions[i - rem_count]['id'] not in institutions_list:
                institutions.pop(i - rem_count)
                rem_count += 1
    return institutions

def get_metadata_collections(inst, creds, log_data):

    url = "{}/{}/jsonContent?types=MetadataCollection&depth=-1".format(
        src_base_url, inst['path'])
    response = requests.get(
        url=url,
        auth=requests.auth.HTTPBasicAuth(
            creds['src_user'], creds['src_pwd'])
    )
    if response.status_code != 200:
        msg = 'Find collections in {} failed -> {}'.format(
            inst['path'], response.status_code)
        log_info(log_data, 'repo', msg)
        # print('{} => []'.format(url))
        return []

    results = json.loads(response.text)
    if len(results) == 0:
        # print('{} => []'.format(url))
        return []

    paths = []
    for result in results:
        if result['id'] == 'templates':
            continue
        paths.append(get_physical_path(result['context_path']))
    # print('{} => {}'.format(url, paths))
    return paths


def create_institution(inst):
    #title_reformatted = re.sub(r'[^a-z0-9_-]+', '-', inst['title'].lower())
    title_reformatted = inst['title']
    #url = "{}/Institutions/jsonCreateInstitution?title={}".format(
    #    ckan_base_url, title_reformatted)
    url = "{}/institutions/".format(ckan_base_url)

    inst_data = {
        "title": title_reformatted,
        "description": ""
    }
    #print("Add inst url {}".format(url))
    response = requests.post(
        url=url,
        #auth=requests.auth.HTTPBasicAuth(
        #    creds['ckan_user'], creds['ckan_pwd'])
        json= inst_data
    )

    #response = requests.post(
    #    url=url,
    #    auth=requests.auth.HTTPBasicAuth(
    #        creds['ckan_user'], creds['ckan_pwd'])
    #)
    if response.status_code != 200:
        result = json.loads(response.text)
        if 'detail' in result:
            msg = result['detail']['name']
        else:
            msg = 'Request failed with return code: %s' % (
                response.status_code)
        return {'error_status': 'failed', 'msg': [{'name': msg}]}

    results = json.loads(response.text)
    return results


def transform_record(record, creds, inst):
    # If no identifier, or dummy identifier, remove the identifier field
    record_id = None
    if isinstance(record['jsonData']['identifier'], dict):
        record_id = record['jsonData']['identifier'].get('identifier')
    if not record_id:
        # If no identifier, set to plone UI
        identifier = record['uid']
        record['jsonData']['identifier'] = {"identifier": identifier, "identifierType": "plone-id"}

    #else:
    #    identifier = record['jsonData']['identifier']['identifier']
    #    if 'DummyDOI' in identifier or 'SAEON_DOI' in identifier:
    #        logging.error("DummyDOI found, removing identifier")
    #        record['jsonData'].pop("identifier")

    resourceType = record['jsonData']['resourceType']
    resourceTypeGeneral = record['jsonData']['resourceTypeGeneral']

    if len(resourceType) != 0:
        record['jsonData']['resourceType'] = {
            'resourceType': resourceType,
            'resourceTypeGeneral': resourceTypeGeneral
        }
    else:
        record['jsonData']['resourceType'] = {
            'resourceType': 'Dataset',
            'resourceTypeGeneral': 'Dataset'#resourceTypeGeneral
        }
    
    if len(record['jsonData']['resourceTypeGeneral']) == 0:
        record['jsonData']['resourceTypeGeneral'] = 'Dataset'

    #print(record['jsonData']['geoLocations'][0].keys())
    # if no geolocations, remove geolocations field
    if len((record['jsonData']['geoLocations'])) == 0:
        record['jsonData'].pop('geoLocations')
    else:
        if (len(record['jsonData']['geoLocations'][0].keys()) > 1):
            print(record['jsonData']['geoLocations'][0])

        locations = []
        if ('geoLocationPoint' in record['jsonData']['geoLocations'][0].keys()):
            geoPoint = record['jsonData']['geoLocations'][0]
            location = {
                    "geoLocationPlace": geoPoint['geoLocationPlace'],   
                    "geoLocationPoint": {
                        "pointLongitude":geoPoint['geoLocationPoint'].split()[1],
                        "pointLatitude": geoPoint['geoLocationPoint'].split()[0]}}
            locations.append(location)        

        if ('geoLocationBox' in record['jsonData']['geoLocations'][0].keys()):
            geoBoxParts = record['jsonData']['geoLocations'][0]['geoLocationBox'].split()
            northBoundLat = geoBoxParts[2] if float(geoBoxParts[2]) > float(geoBoxParts[0]) else geoBoxParts[0]
            southBoundLat = geoBoxParts[0] if float(geoBoxParts[2]) > float(geoBoxParts[0]) else geoBoxParts[2]
            westBoundLon = geoBoxParts[1] if float(geoBoxParts[1]) < float(geoBoxParts[3]) else geoBoxParts[3]
            eastBoundLon = geoBoxParts[3] if float(geoBoxParts[1]) < float(geoBoxParts[3]) else geoBoxParts[1]
        
            location = {
                'geoLocationBox': {
                    'northBoundLatitude': northBoundLat,
                    'southBoundLatitude': southBoundLat,
                    'westBoundLongitude': westBoundLon,
                    'eastBoundLongitude': eastBoundLon}}
            locations.append(location)
        
        if len(locations) > 0:
            record['jsonData']['geoLocations'] = locations
        else:
            # if no geolocations, remove geolocations field
            record['jsonData'].pop('geoLocations')

    coverageBegin = record['jsonData']['additionalFields']['coverageBegin']
    coverageEnd = record['jsonData']['additionalFields']['coverageEnd']
    if (len(coverageEnd) > 0):
        record['jsonData']['dates'].append({"date" : coverageEnd, "dateType": "Valid"})
    if (len(coverageBegin) > 0):
        record['jsonData']['dates'].append({"date" : coverageBegin, "dateType": "Collected"})

    def check_date_format(date_str, format_str):
        valid = True
        try:
            datetime.strptime(date_str, format_str)
        except ValueError:
            valid = False
        return valid

    del_ind = []
    for i in range(len(record['jsonData']['dates'])):
        if len(record['jsonData']['dates'][i]['date']) == 0:
            del_ind.append(i)
        else:
            d = record['jsonData']['dates'][i]['date']
            year_only_valid = check_date_format(d, '%Y-%m-%d')
            full_date_valid = check_date_format(d, '%Y')
            if not year_only_valid and not full_date_valid:
                logging.error("Invalid date format, removing {}".format(d))
                del_ind.append(i)

    for i in range(len(del_ind)):
        record['jsonData']['dates'].pop(del_ind[i] - i*1)

    def get_publication_year(datestr,format):
        year = None
        try:
            year = datetime.strptime(datestr, format)
            year = year.year
        except Exception as e:
            pass
        return year

    pub_year = None
    publication_str = record['jsonData']['publicationYear']
    pub_year = get_publication_year(publication_str, '%Y')
    if not pub_year:
        pub_year = get_publication_year(publication_str, '%Y-%m-%d')
        #pub_year = pub_year.year
    
    # if pub year is still none, default to 2018
    if not pub_year:
        record['jsonData']['publicationYear'] = '2018'
    else:
        record['jsonData']['publicationYear'] = str(pub_year)

    record['jsonData']['alternateIdentifiers'] = [{
        "alternateIdentifier":record['uid'],
        "alternateIdentifierType": "Plone"}]

    # if no description, blank it out
    if (len(record['jsonData']['description']) == 0):
        record['jsonData']['description'] = [{
            'description':''}]

    record['jsonData']['descriptions'] = []
    record['jsonData']['descriptions'].append({
        'descriptionType': 'Abstract',#record['jsonData']['description'][0]['descriptionType'],
        'description': record['jsonData']['description'][0]['description']})

    # remove old description field
    if 'description' in record['jsonData']:
        record['jsonData'].pop('description')

    # if no rights then blank it out
    if (len(record['jsonData']['rights']) == 0):
        record['jsonData']['rights'] = [{
            'rights': '',
            'rightsURI': ''}]

    record['jsonData']['rightsList'] = [
        {
            'rights': record['jsonData']['rights'][0]['rights'],
            'rightsURI': record['jsonData']['rights'][0]['rightsURI']
        }
    ]

    rightsURI = record['jsonData']['rightsList'][0]['rightsURI'] 
    if not rightsURI or rightsURI == 'none':
        if inst['path'] != 'Institutions/chief-directorate-national-geo-spatial-information':
            record['jsonData']['rightsList'][0]['rightsURI'] = 'https://creativecommons.org/licenses/by/4.0/'
        else:
            record['jsonData']['rightsList'][0]['rightsURI'] = '' 

    immutable_resource = None
    linked_resources = []
    for resource in record['jsonData']['additionalFields']['onlineResources']:
        if (not immutable_resource) and (resource['func'] == 'download'):
            immutable_resource = resource
        else:
            linked_resources.append(resource)
    # if no immutable resource then remove immutable resource field
    if not immutable_resource:
        msg = "Immutable resource url not available!"
        logging.info(msg)
        record['jsonData']['immutableResource'] = {"resourceURL": "download link unavailable"}
        #record['jsonData'].pop('immutableResource')
        #logging.info(record['jsonData'])
    else:
        record['jsonData']['immutableResource'] = {
            "resourceURL": immutable_resource['href'],
            "resourceDescription": immutable_resource['desc']
        }
        # if resource url is blank, remove the immutable resource field
        immutable_url = record['jsonData']['immutableResource']['resourceURL']
        if not immutable_url or len(immutable_url) == 0:
            record['jsonData']['immutableResource'] = {"resourceURL": "download link unavailable"}
        
    record['jsonData']['linkedResources'] = []
    linked_res_mappings = {
        'information':'Information',
        'service':'Query',
        'download':'Query',
        'Data Link':'Query',
        'Related Link':'Query',
        'metadata':'Metadata',
        'Link':'Information',
        'order':'ConditionalAccess',
        'originalmetadata':'Metadata'
    }
    for linked_res in linked_resources:
        #if linked_res['func'] == 'order':
        #    print(record['jsonData']['additionalFields']['onlineResources'])
        record['jsonData']['linkedResources'].append({
            "linkedResourceType": linked_res_mappings[linked_res['func']],
            "resourceURL": linked_res['href'],
            "resourceDescription": linked_res['desc']     
        })

    record['jsonData']['language'] = 'en-US'

    # Remove duplicate subjects
    subjects = []
    duplicate_subjects = []
    new_subjects = []
    for subject in record['jsonData']['subjects']:
        curr_sub = subject['subject']
        skip = False
        for new_sub in new_subjects:
            if curr_sub == new_sub['subject']:
                #print("Duplicate! {}".format(curr_sub))
                skip = True
                break
        if not skip:
            new_subjects.append(subject)    
    record['jsonData']['subjects'] = new_subjects
    #print(new_subjects)

    valid_contrib_types = [
        'ContactPerson', 'DataCollector', 'DataCurator', 'DataManager', 
        'Distributor', 'Editor', 'HostingInstitution', 'Producer',
        'ProjectLeader', 'ProjectManager', 'ProjectMember',
        'RegistrationAgency','RegistrationAuthority', 'RelatedPerson',
        'Researcher', 'ResearchGroup', 'RightsHolder', 'Sponsor',
        'Supervisor', 'WorkPackageLeader', 'Other']

    funding_refs = []
    contrib_i_to_remove = []
    i = 0
    contributors = record['jsonData']['contributors']
    for contrib in contributors:
        # if no contrib type set it to Other
        if 'contributorType' not in contrib:
            contrib['contributorType'] = 'Other'
        contrib_type = contrib['contributorType']        
        if contrib_type == 'Funder':
            funding_refs.append(contrib['contributorName'])
            contrib_i_to_remove.append(i)
        elif contrib_type.replace(" ","") in valid_contrib_types:
            contrib['contributorType'] = contrib_type.replace(" ","")
        elif contrib_type not in valid_contrib_types:
            logging.info("Unsupportd contibutor type {}".format(contrib_type))
            contrib['contributorType'] = 'Other'
        i+=1
    # Remove Funder contributor and add as fundingReference field
    for i in range(len(contrib_i_to_remove)):
        record['jsonData']['contributors'].pop(contrib_i_to_remove[i] - i)
    funding_refs_formatted = []
    for funding_ref in funding_refs:
        funding_refs_formatted.append({"funderName":funding_ref})
    record['jsonData']['fundingReferences'] = funding_refs_formatted

    # Map contributors to new metadata format
    if len(record['jsonData']['contributors']) > 0:
        contributors = record['jsonData']['contributors']
        new_contributors = []
        for contributor in contributors:
            contributorName = contributor["contributorName"] if "contributorName" in contributor else ""
            organisation = contributor["organisation"] if "organisation" in contributor else ""
            contributorType = contributor["contributorType"] if "contributorType" in contributor else ""
            affiliation = contributor["affiliation"] if "affiliation" in contributor else ""

            new_contributor_mapping = {
                    "contributorType": contributorType,
                    "name": contributorName,
                    "givenName": "",
                    "familyName": "",
                    "nameIdentifiers": [
                        {
                            "nameIdentifier": "",
                            "nameIdentifierScheme": "",
                            "schemeURI": ""
                        }
                    ],
                    "affiliations": [
                        {
                            "affiliation": affiliation
                        }
                    ]
                }
            new_contributors.append(new_contributor_mapping)
        record['jsonData']['contributors'] = new_contributors
    
    #if len(contrib_i_to_remove) > 0:
    #    print("Removed mandigno")
    #    print(record['jsonData']['contributors'])
    creators = record['jsonData']['creators']
    if not creators or len(creators) == 0:
        inst_title = '{}'.format(inst['title'])
        record['jsonData']['creators'] = [{"creatorName":inst_title, "affiliation":inst_title}]
    elif len(creators[0]['creatorName']) == 0:
        record['jsonData']['creators'][0]['creatorName'] = inst['title']
    elif len(creators) > 0:
        for creator in creators:
            if len(creator["affiliation"]) == 0:
                creator["affiliation"] = inst['title']
    
    remapped_creators = []
    for creator in record['jsonData']['creators']:
        affiliation = creator["affiliation"] if "affiliation" in creator else ""
        creatornName = creator["creatorName"] if "creatorName" in creator else ""
        nameIdentifier = creator["nameIdentifier"] if "nameIdentifier" in creator else ""
        nameIdentifierScheme = creator["nameIdentifierScheme"] if "nameIdentifierScheme" in creator else ""
        schemeURI = creator["schemeURI"] if "schemeURI" in creator else ""
        remapped_creator =  {
            "name": creatornName,
            "nameType": "",
            "givenName": "",
            "familyName": "",
            "nameIdentifiers": [
                {
                    "nameIdentifier": nameIdentifier,
                    "nameIdentifierScheme": nameIdentifierScheme,
                    "schemeURI": schemeURI
                }
            ],
            "affiliations": [
                {
                    "affiliation": affiliation
                }
            ]
        }
        remapped_creators.append(remapped_creator)
    duplicate_indeces = []
    for creator in remapped_creators:
        matches = 0
        index = 0
        for c in remapped_creators:
            if str(creator) == str(c):
                matches += 1
                if matches > 1:
                    duplicate_indeces.append(index)
            index += 1
    duplicate_indeces = list(set(duplicate_indeces))
    for i in range(len(duplicate_indeces)):
        remapped_creators.pop(duplicate_indeces[i] - i*1)
    record['jsonData']['creators'] = remapped_creators

    publisher = record['jsonData']['publisher']
    if not publisher or len(publisher) == 0:
        record['jsonData']['publisher'] = '{}'.format(inst['title'])

    record['jsonData']['originalMetadata'] = download_xml(record['url'], creds)
    #if (len(record['jsonData']['original_xml']) > 0):
    #    print('### original xml ###')
    #    print(record['jsonData'])
        #print(record['jsonData']['original_xml'])


    if 'xsiSchema' in record['jsonData'] and len(record['jsonData']['xsiSchema']) > 0:
        xsiSchema = record['jsonData']['xsiSchema']
        relatedIdentifier = {
            "relatedIdentifier": xsiSchema,
            "relatedIdentifierType": "URL",
            "relationType": "HasMetadata",
            "schemeType":xsiSchema
        }
        record['jsonData']['relatedIdentifiers'].append(relatedIdentifier)

    inv_keys = ['dataSchema', 'rights', 'resourceTypeGeneral', 'xsiSchema', 'schemaSpecific', 
                'additionalFields', 'bounds', 'errors', 'title']
    for k in inv_keys:
        if k in record['jsonData']:
            record['jsonData'].pop(k)

    return record['jsonData']


def log_info(log_data, atype, msg):
    if not log_data.get(atype):
        log_data[atype] = []
    log_data[atype].append(msg)

def check_record_empty(record):
    empty_key_igore_list = ['language','alternateIdentifiers', 'original_xml', 
                            'errors' ,'linkedResources', 'additionalFields']
    empty_cases = [ 
        'None',
        [{'description': 'none'}],
        [{'date': '', 'dateType': 'Collected'}],
        [{'rights': 'none', 'rightsURI': 'none'}],
        {'resourceType': '', 'resourceTypeGeneral': 'Dataset'},
        [{'descriptionType': 'Abstract', 'description': 'none'}],
        [{'rights': 'none', 'rightsURI': 'none'}]
    ]
    all_empty = True
    for key in record.keys():
        if key not in empty_key_igore_list:
            val = record[key]
            if val or len(val) > 0:
                #all_empty = False
                if val not in empty_cases:
                    all_empty = False
                    #print("non empty value {}".format(val))
    return all_empty


def import_metadata_records(inst, creds, paths, log_data, ids_to_import):
    for path in paths:
        records = get_metadata_records(path, creds)
        
        if records.startswith('Request failed'):
            msg = '\n### {}: {}\n'.format(path, records)
            log_info(log_data, 'import', msg)
            logging.error(msg)
            continue
        if records.startswith('There is nothing here'):
            msg = '\n### Unauthorised to access {}\n'.format(path)
            log_info(log_data, 'import', msg)
            logging.error(msg)
            continue
        records = json.loads(records)
        if len(records['content']) == 0:
            msg = '### No records found in {}'.format(path)
            log_info(log_data, 'import', msg)
            logging.error(msg)
            continue       

        if import_to_ckan:
            response = create_institution(inst)
            print("response {}".format(response))

            if 'error_status' in response and \
                response['error_status'] == 'failed' and \
                'message' in response['msg'][0] and \
                response['msg'][0]['message'].startswith(
                    'Access denied'):
                msg = '\n### Access denied! Could not add institution %s\n' %(inst)
                logging.error(msg)
                logging.error(response['msg'])
                #print(msg)
                
                log_info(log_data,'institution', msg)  
                log_info(log_data, 'institution', response['msg'])                
                continue
            #print("add inst response {}".format(response))
            if 'error_status' in response and \
                response['error_status'] == 'failed' and \
                not response['msg'][0]['name'][0].startswith(
                    'Group name already exists in database'):
                log_info(log_data, 'institution', response['msg'])
                logging.error("Could not add institution: {}".format(inst))
                logging.error(response['msg'])                
                continue
            elif 'error_status' in response and \
                response['error_status'] == 'failed' and \
                response['msg'][0]['name'][0].startswith(
                    'Group name already exists in database'):
                logging.error("Could not add institution: {}".format(inst))
                logging.error(response['msg'])
        
        UPDATE_METRICS['update_count'] = UPDATE_METRICS['update_count'] + len(records['content'])
                
        for record in records['content']:

            # if uids to import are provided, only import record with uid in given list
            if len(ids_to_import) > 0:
                #print(record['uid'])
                #print(uids_to_import[0])
                #sys.exit(1)
                if len(record['jsonData']['identifier']) > 0:
                    current_id = record['jsonData']['identifier']['identifier']                                
                    #print(current_id)     
                    if current_id not in ids_to_import:
                        #print(uids_to_import[0])
                        #logging.info("Skipping record {}, not in provided uid list".format(record['uid']))
                        continue
                    else:
                        logging.info("Importing record {}, provided uid list".format(record['jsonData']['identifier']))
                else:
                    #logging.error("Skipping invalid record")
                    continue
            # check if all record values are empty
            if check_record_empty(record['jsonData']):
                logging.error("All metadata fields are empty, skipping record ...")
                continue

            #print(record['uid'])#['contributorType'])   
            record_id = None
            if isinstance(record['jsonData']['identifier'], dict):
                record_id = record['jsonData']['identifier'].get('identifier')
            """
            if not record_id:                
                #record_id = gen_unique_id()
                msg = "No DOI identifier, skipping record!"
                log_info(log_data,'record_id', msg)
                #logging.error(msg)
                #print("InstError {} url {}".format(record['institution'], record['url']))
                immutable_resource = None
                linked_resources = []
                for resource in record['jsonData']['additionalFields']['onlineResources']:
                    if (not immutable_resource) and (resource['func'] == 'download'):
                        immutable_resource = resource
                    else:
                        linked_resources.append(resource)
                
                if not immutable_resource or len(immutable_resource['href']) == 0:
                    logging.error("No DOI, and no immutable resource, skipping record! Links{}".format(linked_resources))
                    #print(linked_resources)
                    continue
                else:
                    logging.info("No DOI, but immutable resource so continuing {}...".format(immutable_resource))
                    #print(immutable_resource)
            """
            #tl = record['jsonData']['titles'][0]['title']
            #if tl != 'Small Area' and tl != 'Main Place':
            #    continue

            # Ignore problematic records
            if record.get('status') not in ['private', 'provisional']:
                log_info(log_data, 'add_record', {
                    'action': 'ignored',
                    'record_id': record_id,
                    'state': record.get('status')})
                msg = 'Invalid record status: {}'.format(record.get('status'))
                logging.error(msg)
                continue

            new_json_data = transform_record(record, creds, inst)

            if not new_json_data:
                msg = "Transform error! Skipping record."
                logging.error(msg)
                continue

            log_info(log_data, 'add_record', {
                'action': 'add',
                'record_id': record_id,
                'state': record.get('status', 'dunno')})
            if False:#import_to_agent:
                add_a_record_to_elastic(
                    record_id=record_id,
                    organization=inst,
                    infrastructures=['SASDI', 'SANSA'],
                    metadata_json=new_json_data,
                    collection='TestImport2',
                )
            #print('plone-{}'.format(record.get('status')))
            if import_to_ckan:
                add_a_record_to_ckan(
                    record_id=record_id,
                    organization=inst,
                    infrastructures=[],
                    metadata_json=new_json_data,#record['jsonData'],
                    collection='',
                    state='plone-{}'.format(record.get('status'))
                    # original_xml??? or is it shipped in metadata_json
                )
            #print(breakpnt)

def read_ids_from_file(ids_file):
    try:
        flines = open(ids_file).readlines()
        ids = []
        for fl in flines:
            #print(fl)
            fl = fl.replace(" ","")
            #id = fl.replace("-","").replace("\n","").replace(" ","")
            id = fl[2:len(fl)-3]            
            ids.append(id)
        return ids
    except Exception as e:
        logging.error("Could not open/read from uids list file.\n{}".format(e))
        return None

def read_institutions_from_file(institutions_file):
    try:
        flines = open(institutions_file).readlines()
        institutions=[]
        for fl in flines:
            fl = fl.replace("\n","")
            institutions.append(fl)
        return institutions
    except Exception as e:
        loggind.error("Could not open/read from institutions file.\n{}".format(e))
        return None

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--src-base-url", required=False, help="the URL for source")
    parser.add_argument("--src-user", required=False, help="user name for source")
    parser.add_argument("--src-pwd", required=True, help="admin password for source")
    parser.add_argument("--import-to-ckan", required=False, help="import metadata to CKAN")
    parser.add_argument("--ckan-base-url", required=False, help="the URL of the CKAN instance")
    parser.add_argument("--ckan-user", required=False, help="user name for ckan")
    parser.add_argument("--ckan-pwd", required=True, help="admin password for ckan")
    parser.add_argument("--import-to-agent", required=False, help="import metadata to the SAEON Metadata Agent")
    parser.add_argument("--agent-base-url", required=False, help="the URL of the SAEON Metadata Agent")
    parser.add_argument("--agent-user", required=False, help="user name for agent")
    parser.add_argument("--agent-pwd", required=True, help="admin password for agent")
    parser.add_argument("--log-file",required=False, help="file to log output to, otherwise output logged to console.")
    parser.add_argument("--id-list-file",required=False, help="ids of records to import, all other records skipped")
    parser.add_argument("--institution-list-file",required=False, help="Institutions to import records from.")

    args = parser.parse_args()
    creds = {
        'src_user': args.src_user or 'admin',
        'src_pwd': args.src_pwd,
        'ckan_user': args.ckan_user or 'admin',
        'ckan_pwd': args.ckan_pwd,
        'agent_user': args.agent_user or 'admin',
        'agent_pwd': args.agent_pwd,
    }
    # print(creds)
    if args.import_to_ckan:
        import_to_ckan = str(args.import_to_ckan).lower() == 'true'
    # print(import_to_ckan)

    if args.import_to_agent:
        import_to_agent = str(args.import_to_agent).lower() == 'true'
    # print(import_to_agent)

    if args.log_file:
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.basicConfig(filename=args.log_file,level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    ids = []
    if args.id_list_file:
        ids = read_ids_from_file(args.id_list_file)
        if (not ids) or (len(ids) == 0):
            logging.error("Could not read valid ids from ids list file")
            sys.exit(1)
        #print(ids)

    institutions_list = None
    if args.institution_list_file:
        institutions_list = read_institutions_from_file(args.institution_list_file)
        if (not institutions_list) or (len(institutions_list) == 0):
            logging.error("Could not read valid institutions from input file")
            sys.exit(1)
    
    institutions = get_institutions(creds, institutions_list)
    
    log_data = {}
    for inst in institutions:
        paths = get_metadata_collections(inst, creds, log_data)
        if paths:
            # added records to inst
            import_metadata_records(inst, creds, paths, log_data, ids)

    # Get states from logged data
    states = {}
    ignored = 0
    added = 0
    for log in log_data.get('add_record', []):
        if log['action'] == 'ignored':
            ignored += 1
        else:
            added += 1

        # Prime dict
        if log['state'] not in states.keys():
            states[log['state']] = 0
        states[log['state']] += 1

    #print('States: {}'.format(states))
    #print('Ignored: {}'.format(ignored))
    #print('Added: {}'.format(added))

    logging.info("\n\nUpdate stats\n{}".format(UPDATE_METRICS))
