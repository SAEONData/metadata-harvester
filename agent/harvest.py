import json
import logging
import os
import requests
from agent import config
from .transformer import transform_record
from .standards import get_unique_identifier

logger = logging.getLogger(__name__)


def _upload_record(result, settings):

    result['upload_error'] = None
    result['upload_success'] = False
    upload_method = settings.get('upload_method')

    data = {
        'metadata_json': json.dumps(result['datacite_data']),
        'owner_org': settings.get('upload_org_name', ''),
        # 'infrastructures': [{'id': 'sansa'}],
        'metadata_collection_id': settings.get('upload_collection', ''),
        'metadata_standard_id': 'datacite-4-2',
        'deserialize_json': 'true',
    }
    if settings.get('upload_index'):
        data['index'] = settings['upload_index']
        data['collection'] = settings.get('upload_collection', '')
        data['organization'] = settings.get('upload_org_name', '')
        data['record_id'] = get_unique_identifier()
        if not result['datacite_data']['identifier']:
            result['datacite_data']['identifier'] = {
                "identifier": data['record_id'],
                # "identifierType": "DOI"
            }
        result['datacite_data'].pop('additionalFields')
        data['metadata_json'] = json.dumps(result['datacite_data'])

    headers = None
    if settings.get('upload_password'):
        headers = {
            'Authorization': settings['upload_password'],
        }
    url = "{}/{}".format(settings['upload_server_url'], upload_method)
    try:
        if headers:
            response = requests.post(
                url=url,
                data=data,
                headers=headers
            )
        else:
            response = requests.post(
                url=url,
                data=data,
            )
    except Exception as e:
        # print(response.text)
        result['upload_error'] = 'Request failed with exception {}.'.format(e)
        logger.info('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result
    if response.status_code != 200:
        # print(response.text)
        result['upload_error'] = 'Request failed with return code: %s' % (
            response.status_code)
        logger.info('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    upload_result = json.loads(response.text)
    if upload_result.get('status') == 'failed' or \
       ('success' in upload_result.keys() and not upload_result.get('success')):
        result['upload_error'] = upload_result.get('msg', 'Unknown')
        logger.info('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    result['upload_success'] = True
    result['upload_result'] = upload_result
    logger.info('Uploaded: {upload_success}'.format(**result))
    return result


def _validate_record(result, settings):

    result['validation_errors'] = []
    result['validation_success'] = False
    validation_method = settings.get(
        'validation_method', 'metadata_record_validate')

    data = {
        'id': result['upload_result']['result']['id']
    }
    headers = {
        'Authorization': settings['upload_password'],
    }
    url = "{}/{}".format(settings['upload_server_url'], validation_method)
    try:
        response = requests.post(
            url=url,
            data=data,
            headers=headers
        )
    except Exception as e:
        # print(response.text)
        result['validation_errors'].append(
            'Request failed with exception {}.'.format(e))
        return result

    if response.status_code != 200:
        result['validation_errors'].append(
            'Request failed with return code: %s' % (response.status_code))
        return result

    validation_result = json.loads(response.text)
    if validation_result.get('status') == 'failed':
        result['validation_errors'].append(
            validation_result.get('msg', 'Unknown'))
        logger.info('Uploader: {validation_success}: {validation_errors}'.format(**result))
        return result

    result['validation_success'] = True
    logger.info('Validation: {validation_success}'.format(**result))
    return result


def _transition_record(result, settings):

    result['transition_errors'] = []
    result['transition_success'] = False
    transition_method = settings.get(
        'transition_method', 'metadata_record_workflow_state_transition')

    data = {
        'id': result['upload_result']['result']['id'],
        'workflow_state_id': 'submit'
    }
    headers = {
        'Authorization': settings['upload_password'],
    }
    url = "{}/{}".format(settings['upload_server_url'], transition_method)
    try:
        response = requests.post(
            url=url,
            data=data,
            headers=headers
        )
    except Exception as e:
        # print(response.text)
        result['transition_errors'].append(
            'Request failed with exception {}.'.format(e))
        return result

    if response.status_code != 200:
        # print(response.text)
        result['transition_error'].append(
            'Request failed with return code: %s' % (response.status_code))
        return result

    transition_result = json.loads(response.text)
    # print(transition_result)
    if transition_result.get('status') == 'failed':
        result['transition_errors'].append(
            transition_result.get('msg', 'Unknown'))
        logger.info('Transition: {transition_success}: {transition_errors}'.format(**result))
        return result

    result['transition_success'] = True
    logger.info('Transition: {transition_success}'.format(**result))
    return result


def _get_metadata_records(settings):
    result = {'records': [], 'errors': []}
    records = None
    transport = settings.get('transport')
    if transport == "FileSystem":
        files = []
        for afile in os.listdir(settings['source_dir']):
            if afile.endswith('.swp'):
                continue
            files.append(afile)
        logger.info('About to process {} files'.format(len(files)))

        if len(files) == 0:
            result['errors'] = \
                'No files in dir {}'.format(settings['source_dir'])
            return result
        records = []
        messages = []
        for filename in files:
            logger.info('Process file {}'.format(filename))
            fullpath = os.path.join(settings['source_dir'], filename)
            if not os.path.isfile(fullpath):
                messages.append('Item {} is not a file'.format(filename))
                continue

            afile = open(fullpath)
            records.append({'title': filename, 'input_data': afile.read()})
            afile.close()

        if messages:
            result['errors'] = messages
            return result

    else:
        msg = 'Harvester transport protocol "{}" not found'.format(transport)
        result['errors'].append(msg)
        return result

    result['records'] = records
    return result


def _harvest_records(settings):
    """
    @summary: does the harvesting for the given type and url
    """
    output = {'success': False, 'records': []}

    logger.info('Harvesting: %s' % settings)
    result = _get_metadata_records(settings)

    records = result['records']
    if records is None or len(records) == 0:
        output['error'] = result['errors']
        return output

    logger.info('Harvester: %s records found in file' % len(records))

    for record in records:
        result = transform_record(record, settings)
        if result['valid']:
            result = _upload_record(result, settings)
        else:
            logger.info('Harvester: Invalid transformation')

        # if result['upload_success']:
        #     result = _validate_record(result, settings)
        # else:
        #     print('Harvester: Upload failed')
        #     continue
        # if result['validated']:
        #     result = _submit_record(result, settings)
        # if result['submitted']:
        #     result = _publish_record(result, settings)
        output['records'].append(result)

    output['success'] = True
    return output


def harvest(kwargs):
    output = {'success': False}
    settings = {}

    if hasattr(config, 'source_dir'):
        settings['source_dir'] = config.source_dir
    if kwargs.get('source_dir'):
        settings['source_dir'] = kwargs.get('source_dir')

        if not os.path.exists(settings['source_dir']):
            output['error'] = 'source_dir {} does not exists'.format(
                settings['source_dir'])
            return output

        files = os.listdir(settings['source_dir'])
        if len(files) == 0:
            output['error'] = 'source_dir {} is empty'.format(
                settings['source_dir'])
            return output

    if hasattr(config, 'transport'):
        settings['transport'] = config.transport
    if kwargs.get('transport'):
        settings['transport'] = kwargs.get('transport')

    if hasattr(config, 'standard'):
        settings['standard'] = config.standard
    if kwargs.get('standard'):
        settings['standard'] = kwargs.get('standard')

    if hasattr(config, 'upload_server_url'):
        settings['upload_server_url'] = config.upload_server_url
    if kwargs.get('upload_server_url'):
        settings['upload_server_url'] = kwargs.get('upload_server_url')

    if hasattr(config, 'upload_user'):
        settings['upload_user'] = config.upload_user
    if kwargs.get('upload_user'):
        settings['upload_user'] = kwargs.get('upload_user')

    if hasattr(config, 'upload_password'):
        settings['upload_password'] = config.upload_password
    if kwargs.get('upload_password'):
        settings['upload_password'] = kwargs.get('upload_password')

    if hasattr(config, 'upload_method'):
        settings['upload_method'] = config.upload_method
    if kwargs.get('upload_method'):
        settings['upload_method'] = kwargs.get('upload_method')

    if hasattr(config, 'upload_org_name'):
        settings['upload_org_name'] = config.upload_org_name
    if kwargs.get('upload_org_name'):
        settings['upload_org_name'] = kwargs.get('upload_org_name')

    if hasattr(config, 'upload_collection'):
        settings['upload_collection'] = config.upload_collection
    if kwargs.get('upload_collection'):
        settings['upload_collection'] = kwargs.get('upload_collection')

    if hasattr(config, 'upload_index'):
        settings['upload_index'] = config.upload_index
    if kwargs.get('upload_index'):
        settings['upload_index'] = kwargs.get('upload_index')

    results = _harvest_records(settings)

    return results
